import json
import os
import subprocess
import time
import zipfile

ACTIVE_TIER = 6  # Set to 6 for GitHub, 7 for Colab/Local
SHARD_SIZE = 50000
BATCH_SIZE = 500
SPLIT_SIZE = "75M"


def log(msg):
    print(msg, flush=True)


def generate_azl_address(n):
    return {
        "n": n,
        "tier": 7,
        "value": n / 1_000_000_000,
        "address": f"AZL-{n:010d}",
        "range": "zero" if n < 1_000_000_000 else "one",
        "law": "N×0=N",
        "proof": "1×1=2",
    }


def main():
    start_time = time.time()
    os.makedirs("output", exist_ok=True)

    # Auto-set total based on tier
    if ACTIVE_TIER == 5:
        total_addresses = 100_000_000
    elif ACTIVE_TIER == 6:
        total_addresses = 1_000_000_000
    else:  # Tier 7
        total_addresses = 10_000_000_000

    total_shards = (total_addresses + SHARD_SIZE - 1) // SHARD_SIZE
    total_batches = (total_shards + BATCH_SIZE - 1) // BATCH_SIZE

    log(f"[AZL] TIER {ACTIVE_TIER} MODE: {total_addresses:,} points")
    log(f"[AZL] Max disk usage: ~500MB")

    current_n = 1
    part_files = []

    for batch_num in range(1, total_batches + 1):
        zip_path = f"output/azl_batch_{batch_num:03d}.zip"
        log(f"[AZL] Building batch {batch_num}/{total_batches}")

        with zipfile.ZipFile(
            zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=1
        ) as zf:
            start_shard = (batch_num - 1) * BATCH_SIZE + 1
            end_shard = min(batch_num * BATCH_SIZE, total_shards)

            for shard_idx in range(start_shard, end_shard + 1):
                # Generate shard in memory, write directly to zip, never touch disk
                shard_data = []
                for i in range(SHARD_SIZE):
                    if current_n > total_addresses:
                        break
                    shard_data.append(
                        json.dumps(generate_azl_address(current_n)) + "\n"
                    )
                    current_n += 1

                shard_content = "".join(shard_data)
                zf.writestr(f"azl_shard_{shard_idx:05d}.jsonl", shard_content)

                if current_n % 5_000_000 == 0:
                    log(f"[AZL] Progress: {current_n:,}")

        # Split the zip
        subprocess.run(
            ["split", "-b", SPLIT_SIZE, "-d", zip_path, f"{zip_path}.part"], check=True
        )
        os.remove(zip_path)  # Delete zip immediately

        # Record parts
        i = 0
        while True:
            part_path = f"{zip_path}.part{i:02d}"
            if not os.path.exists(part_path):
                break
            part_files.append(part_path)
            i += 1

        log(f"[AZL] Batch {batch_num} done. Parts on disk: {len(part_files)}")

    manifest = {
        "tier": ACTIVE_TIER,
        "law": "N×0=N",
        "proof": "1×1=2",
        "total_addresses": total_addresses,
        "total_parts": len(part_files),
        "shard_files": [os.path.basename(p) for p in part_files],
    }

    with open("output/azl_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    elapsed = time.time() - start_time
    log(f"[AZL] COMPLETE: {len(part_files)} parts in ./output/")
    log(f"[AZL] Time: {elapsed/60:.1f} minutes")
    log(f"[AZL] Final disk used: ~{len(part_files) * 75}MB")


if __name__ == "__main__":
    main()

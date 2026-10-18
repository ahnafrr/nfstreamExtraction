"""
Extracting flow features from PCAP files using nfstream.

How to use:
    python extract_nfstream.py <input.pcap> <output.csv>
"""
import sys

from nfstream import NFStreamer

def main(pcap_path, csv_path):
    streamer = NFStreamer(
        source=pcap_path,  # PCAP file (Ethernet format)
        statistical_analysis=True,  # +48 statistical features (packet size, IAT, TCP flags)
        idle_timeout=120,  # flow is closed if no packet for 120 seconds (default)
        active_timeout=1800,  # long flow is cut every 1800 seconds (default)
    )
    df = streamer.to_pandas()
    if df is None or len(df) == 0:
        sys.exit(
            "No flow found. Check if the PCAP is in Ethernet format "
            "(see Phase 2) and the file path is correct."
        )
    df.to_csv(csv_path, index=False)
    print(f"Total flow   : {len(df)}")
    print(f"Number of columns : {len(df.columns)}")
    print(f"Saved to  : {csv_path}")

# MANDATORY on Windows: nfstream uses multiprocessing; without this block,
# The script will error / run repeatedly when child processes are created.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

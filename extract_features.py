# extract_features.py
# This script uses Scapy to read all PCAP files matching the pattern "ns3_simulation-*.pcap"
# and extracts basic features from each IP packet, saving the results into CSV files.

from scapy.all import rdpcap, IP
import csv
import glob

def extract_features(pcap_file, output_csv):
    # Load the PCAP file
    packets = rdpcap(pcap_file)
    
    # Initialize an empty list to store extracted features
    features = []
    
    # Loop over each packet in the PCAP file
    for pkt in packets:
        # Check if the packet contains an IP layer
        if IP in pkt:
            # Extract source IP, destination IP, protocol, and packet length
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            protocol = pkt[IP].proto
            pkt_length = len(pkt)
            
            # Append the extracted features to our list
            features.append([src_ip, dst_ip, protocol, pkt_length])
    
    # Write the extracted features to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write a header row
        writer.writerow(['Source IP', 'Destination IP', 'Protocol', 'Packet Length'])
        # Write each packet's features
        writer.writerows(features)
    
    print(f"Features have been extracted and saved to {output_csv}")

if __name__ == "__main__":
    # Use glob to find all PCAP files that match the naming pattern.
    pcap_files = glob.glob("PCAP/ns3_simulation-*.pcap")
    print(f"Found PCAP files: {pcap_files}")
    
    # Process each PCAP file
    for pcap_file in pcap_files:
        # Create an output CSV filename by replacing .pcap with .csv
        output_csv = pcap_file.replace("PCAP", "FEATURES").replace(".pcap", ".csv")
        extract_features(pcap_file, output_csv)

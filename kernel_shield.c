#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <bpf/bpf_helpers.h>

// High-speed kernel map to store blacklisted malicious IPs
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, __u32);     // IP Address
    __type(value, __u32);   // Drop flag
} blacklisted_ips SEC(".maps");

SEC("xdp")
xdp_drop_malicious(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    
    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    // Check if packet is IPv4
    if (eth->h_proto != __constant_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *iph = data + sizeof(struct ethhdr);
    if ((void *)(iph + 1) > data_end)
        return XDP_PASS;

    // Lookup IP in kernel blacklist map
    __u32 ip_src = iph->saddr;
    __u32 *is_blocked = bpf_map_lookup_elem(&blacklisted_ips, &ip_src);

    if (is_blocked) {
        // Drop packet instantly at NIC hardware/driver level (0 CPU Overhead)
        return XDP_DROP;
    }

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
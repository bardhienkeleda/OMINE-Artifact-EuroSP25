for iface in $(ip -o link show | awk -F': ' '{print $2}' | cut -d'@' -f1 | grep -E '^s[0-9]+-eth[0-9]+$' | sort -u); do
    echo "Deleting $iface"
    sudo ip link delete "$iface"
done
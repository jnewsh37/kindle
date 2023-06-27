ssh kindle "cd /; ./usr/bin/dm.sh; cd /mnt/us/documents; batteryinfovar=$(grep "battinfo" all_system_logs* | tail -1); blevelvar=$(echo $batteryinfovar|cut -f4 -d " "); echo $blevelvar"

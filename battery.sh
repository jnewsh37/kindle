ssh kindle 'cd /; 
  rm -r /mnt/us/documents/all_*; 
  rm -r /mnt/us/documents/wininfo*; 
  ./usr/bin/dm.sh >/dev/null 2>/dev/null; 
  cd /mnt/us/documents; 
  batteryinfovar=$(grep "battinfo" all_system_logs* | tail -1); 
  blevelvar=$(echo $batteryinfovar|cut -f4 -d " ");
  blevelvar=${blevelvar:17};
  blevelvar=$(echo "$blevelvar"| sed 's/.$//')
  echo $blevelvar'

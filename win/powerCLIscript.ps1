Connect-VIServer "vcenter-01.smk.dk" -User "smk\????" -Password "?????????"
$allvms = @()
$allhosts = @()
$hosts = Get-VMHost
$vms = Get-Vm

foreach($vm in $vms){

  $statdisk = Get-Stat -Entity ($vm)-start (get-date).AddDays(-30) -Finish (Get-Date) -stat disk.usage.average -IntervalMins 3

  $disk = $statdisk

  $allvms += $disk + "Name:" + $vm
}
$allvms | Out-File -Encoding UTF8 "N:\tmp\VMs.txt"

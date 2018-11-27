#This Script shuts down all Server (powerState ne Off) on an emergency
#Author: Ulrich Pollak

Import-Module HPOneView.410

#Connect-HPOVMgmt -Hostname 10.167.0.103 -UserName Administrator -Password password

$arrServers = Get-HPOVServer

Write-Host "Initiating Emergency Shutdown" -ForegroundColor Red


foreach ($server in $arrServers) {

  if($server.powerState -ne "Off") {
    Stop-HPOVServer -InputObject $server  -Confirm:$false
    Write-Host "Server Shutdown:" $server.name -ForegroundColor Yellow
  }

}

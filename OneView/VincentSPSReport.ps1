Import-Module HPOneView.410

Connect-HPOVMgmt -Hostname 192.168.2.50 -UserName Administrator -Password password

foreach ($server in Get-HPOVServer) {
    $fw = Send-HPOVRequest $server.serverFirmwareInventoryUri
    Write-Output ("Server " + $server.name + " is running SPS firmware " + ($fw.components | Where-Object componentName -Like '*SPS*').componentVersion )
}

Disconnect-HPOVMgmt

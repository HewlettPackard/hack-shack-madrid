##############################################################################9
## (C) Copyright 2017-2018 Hewlett Packard Enterprise Development LP 
##############################################################################
<#
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
#>

[CmdletBinding()]
Param
(
    [Parameter(Mandatory)]
    [string]$Portal,

    [Parameter(Mandatory)]
    [string]$Username,

    [Parameter(Mandatory)]
    [string]$Password
    
)

$ErrorActionPreference = 'Continue'

import-module hpeonesphere.psm1


$secpasswd = ConvertTo-SecureString $Password -AsPlainText -Force
$Global:mycreds = New-Object System.Management.Automation.PSCredential ($Username, $secpasswd)

Connect-HPEOS -portal $Portal  -credentials $mycreds

# Get stuff
$zones = Get-hpeoszone
$deployments = get-hpeosdeployment
$projects = get-hpeosproject
$providers = get-hpeosprovider
$deployments = get-hpeosdeployment
$regions = get-hpeosregion

$i=@{}

$i[0]={}

clear
write-host -foregroundcolor green "Zone`t`t`tRegion`t`t`tProvider`t`t`tZone`t`t`tDeployment`t`tProject"

foreach ($zone in $zones) {
    $provider=$providers | where uri -eq $zone.provideruri  
    $region=$regions | where uri -eq $zone.regionuri
    $zonetype = ($zone.zonetypeuri).split("/")[3]

    foreach ($deployment in $deployments) {   
        if ($deployment.zoneuri -eq $zone.uri) {
            $project=$projects | where uri -eq $deployment.projecturi
            write-host -nonewline "$($zone.name)`t`t$($region.name)`t`t$($provider.name)`t`t$zonetype"
            write-host -foregroundcolor red -nonewline "`t`t$($deployment.name)"
            write-host -foregroundcolor yellow "`t`t$($project.name)"
        }
    }
    write-host                
}


# Disconnect
#disconnect-hpeos



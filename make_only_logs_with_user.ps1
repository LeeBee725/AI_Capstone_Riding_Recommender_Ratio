$newLogDir = './only_logs_with_user'
[void](New-Item -Force -Path $newLogDir -ItemType Directory)

$oldLogDir = "./log"
$HISTORY_LOG = 'HistoryLog'
$userName = Get-ChildItem -Path $oldLogDir -Name
'Total Time = {0}M' -f (Measure-Command {
	$userName | Foreach-Object -Parallel {
		if (Test-Path "$using:oldLogDir/$_/$using:HISTORY_LOG/") {
			[void](New-Item -Force -Path "$using:newLogDir/$_" -ItemType Directory)
			$user = $_
			Get-ChildItem -Path "$using:oldLogDir/$_/$using:HISTORY_LOG/" -Name | Foreach-Object {
				Copy-Item -Force -Filter '*.log' -Path "$using:oldLogDir/$user/$using:HISTORY_LOG/$_" -Destination "$using:newLogDir/$user/$_"
			}
			Write-Host "$_ is done!"
		} elseif (Test-Path "$using:oldLogDir/$_/*.log") {
			[void](New-Item -Force -Path "$using:newLogDir/$_" -ItemType Directory)
			$user = $_
			Get-ChildItem -Path "$using:oldLogDir/$_/" -Name | Foreach-Object {
				Copy-Item -Force -Filter '*.log' -Path "$using:oldLogDir/$user/$_" -Destination "$using:newLogDir/$user/$_"
			}
			Write-Host "$_ is done!"
		} else {
			Write-Host "$_ doesn't have log!"
		}
	} -ThrottleLimit 4
}).TotalMinutes
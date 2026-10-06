$nomeSemExtensao = (Get-Item $PSCommandPath).BaseName
py "$PSScriptRoot\$nomeSemExtensao" @args

$Env:CONDA_EXE = "C:\End-to-End-Medical-Chatbot\Miniconda\Scripts\conda.exe"
$Env:_CE_M = $null
$Env:_CE_CONDA = $null
$Env:_CONDA_ROOT = "C:\End-to-End-Medical-Chatbot\Miniconda"
$Env:_CONDA_EXE = "C:\End-to-End-Medical-Chatbot\Miniconda\Scripts\conda.exe"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs
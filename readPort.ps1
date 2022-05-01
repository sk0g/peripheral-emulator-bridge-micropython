[System.IO.Ports.SerialPort]::getportnames()
$port = New-Object System.IO.Ports.SerialPort COM4, 9600, None, 8, one
$port.open()
$port.WriteLine("Hello\n")
Write-Output $port.ReadExisting()
$port.Close()
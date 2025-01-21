# StartChromeDebug.ps1

# Kontrol mekanizması ekleyin, eğer Chrome zaten çalışıyorsa tekrar çalıştırmaz
if (Get-Process -Name "chrome" -ErrorAction SilentlyContinue) {
    Write-Output "Chrome daha onceden baslatildigi icin onceki tarayici kapatiliyor.." 
	Stop-Process -Name chrome -Force
	#Kapatmak istemez isek exit yapıp işlemi sonlandırırız.
}

# Chrome'u debug modunda başlat
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$debugPort = 9222
$userDataDir = "C:\chrome_debug_profile"

Start-Process $chromePath -ArgumentList "--remote-debugging-port=$debugPort", "--user-data-dir=$userDataDir"

Write-Output "Chrome debug modunda baslatildi."

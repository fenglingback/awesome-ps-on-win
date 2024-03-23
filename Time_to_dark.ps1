# 设置全局变量
$monitor = Get-WmiObject -Namespace root/wmi -Class wmiMonitorBrightnessMethods

# 更改亮度值
$monitor.WmiSetBrightness(6, 20)
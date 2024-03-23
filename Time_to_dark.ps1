# 设置全局变量
$monitor = Get-WmiObject -Namespace root/wmi -Class wmiMonitorBrightnessMethods

# 更改亮度值（在6秒内把显示屏的亮度调到20%）
$monitor.WmiSetBrightness(6, 20)
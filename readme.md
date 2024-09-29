每个设置的含义如下：

MINTEMP：风扇开始旋转的最低温度。低于此温度时，风扇将保持关闭状态。
MAXTEMP：风扇应以最大速度运转的温度。高于此温度时，风扇将全速运转。
MINSTART：风扇可以启动的最小 PWM 值。低于某个速度时风扇可能无法开始旋转。
MINSTOP：风扇停止旋转的 PWM 值。

配置示例：
对于每个风扇输出（例如hwmon5/pwm1），您可以配置基于温度的风扇控制。以下是示例设置：

MINTEMP = 40°C（当温度达到 40°C 时风扇开始旋转）
MAXTEMP = 80°C（当温度达到80°C时，风扇以最大速度运转）
MINSTART = 100（启动风扇的最小 PWM 值）
MINSTOP = 20（当PWM低于此值时风扇停止）

Found the following devices:
   hwmon0 is acpitz
   hwmon1 is nvme
   hwmon2 is asus
   hwmon3 is iwlwifi_1
   hwmon4 is coretemp
   hwmon5 is nct6798

Found the following PWM controls:
   hwmon5/pwm1           current value: 255
   hwmon5/pwm2           current value: 255
   hwmon5/pwm3           current value: 255
   hwmon5/pwm4           current value: 255
   hwmon5/pwm6           current value: 255
   hwmon5/pwm7           current value: 255
sudo pwmconfig


run

sudo pwmconfig

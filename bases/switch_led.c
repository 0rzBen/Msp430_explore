#include <msp430.h> 

//按下开关点灯

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // 停止看门狗定时器

    P1DIR |= BIT0;              // 将 P1.0 设置为输出（连接 LED）
    P1REN |= BIT1;              // 启用 P1.1 的内部上拉/下拉电阻
    P1OUT |= BIT1;              // 将 P1.1 设置为上拉电阻


    while(1)
    {
        if (P1IN & BIT1)        // 如果 P1.1 输入高电平（按键未按下）

            P1OUT &= ~BIT0;     // 熄灭 LED（P1.0 输出低电平）

        else                    // 如果 P1.1 输入低电平（按键按下）

            P1OUT |= BIT0;      // 点亮 LED（P1.0 输出高电平）

    }
}


#ifndef __OLED_H
#define __OLED_H
 
#include <msp430.h>
#include "OLED_type.h"
 
#define OLED_MODE 0
#define SIZE 8
#define XLevelL     0x00
#define XLevelH     0x10
#define Max_Column  128
#define Max_Row     64
#define Brightness  0xFF
#define X_WIDTH     128
#define Y_WIDTH     64
 
#define OLED_SCLK_Clr() P3OUT &= ~BIT5  //SCL
#define OLED_SCLK_Set() P3OUT |= BIT5
 
#define OLED_SDIN_Clr() P3OUT &= ~BIT6  //SDA
#define OLED_SDIN_Set() P3OUT |= BIT6
 
#define OLED_CMD    0
#define OLED_DATA   1
 
void Picture();
void IIC_Stop();
void IIC_Start();
void IIC_Wait_Ack();
void OLED_Init(void);
void OLED_Clear(void);
void OLED_Clearlines(u8 s, u8 e);
void OLED_Display_On(void);
void Delay_1ms(u16 Del_1ms);
void OLED_Display_Off(void);
void OLED_Set_Pos(u8 x, u8 y);
void fill_picture(u8 fill_Data);
void Write_IIC_Data(u8 IIC_Data);
void Write_IIC_Byte(u8 IIC_Byte);
void OLED_DrawPoint(u8 x,u8 y,u8 t);
void Write_IIC_Command(u8 IIC_Command);
void OLED_ShowCHinese(u8 x,u8 y,u8 no);
void OLED_ShowVI(u8 x,u8 y,u32 num,u8 size);
void OLED_WR_Byte(unsigned dat,unsigned cmd);
void OLED_Fill(u8 x1,u8 y1,u8 x2,u8 y2,u8 dot);
void OLED_ShowChar(u8 x,u8 y,u8 chr,u8 Char_Size);
void OLED_ShowNum(u8 x,u8 y,u32 num,u8 len,u8 size);
void OLED_ShowString(u8 x,u8 y, u8 *p,u8 Char_Size);
void OLED_DrawBMP(u8 x0, u8 y0,u8 x1, u8 y1,u8 BMP[]);
 
#endif


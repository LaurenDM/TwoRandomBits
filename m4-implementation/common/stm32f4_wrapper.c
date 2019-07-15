#include "stm32wrapper.h"

/* 24 MHz */
const struct rcc_clock_scale myclock = {
    //HSE = 8 MHz
    .pllm = 8, //VCOin = HSE / PLLM = 1 MHz
    .plln = 192, //VCOout = VCOin * PLLN = 192 MHz
    .pllp = 8, //PLLCLK = VCOout / PLLP = 24 MHz (low to have 0WS)
    .pllq = 4, //PLL48CLK = VCOout / PLLQ = 48 MHz (required for USB, RNG)
    .hpre = RCC_CFGR_HPRE_DIV_NONE,
    .ppre1 = RCC_CFGR_PPRE_DIV_2,
    .ppre2 = RCC_CFGR_PPRE_DIV_NONE,
    .flash_config = FLASH_ACR_LATENCY_0WS,
    .apb1_frequency = 12000000,
    .apb2_frequency = 24000000,
};


void clock_setup(void)
{
    rcc_clock_setup_hse_3v3(&myclock);
    rcc_periph_clock_enable(RCC_GPIOC);
    rcc_periph_clock_enable(RCC_USART3);
    rcc_periph_clock_enable(RCC_CCMDATARAM);
    rcc_periph_clock_enable(RCC_RNG);
}

void gpio_setup(void)
{
    gpio_mode_setup(GPIOC, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO10 | GPIO11);
    gpio_set_af(GPIOC, GPIO_AF7, GPIO10 | GPIO11);

    gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, GPIO2);
}

void usart_setup(int baud)
{
    usart_set_baudrate(USART3, baud);
    usart_set_databits(USART3, 8);
    usart_set_stopbits(USART3, USART_STOPBITS_1);
    usart_set_mode(USART3, USART_MODE_TX_RX);
    usart_set_parity(USART3, USART_PARITY_NONE);
    usart_set_flow_control(USART3, USART_FLOWCONTROL_NONE);

    usart_enable(USART3);
}

void flash_setup(void)
{
    FLASH_ACR |= FLASH_ACR_ICEN;
    FLASH_ACR |= FLASH_ACR_DCEN;
    FLASH_ACR |= FLASH_ACR_PRFTEN;
}

void send_USART_str(const char* in)
{
    int i;
    for(i = 0; in[i] != 0; i++) {
        usart_send_blocking(USART3, (unsigned char)in[i]);
    }
    usart_send_blocking(USART3, '\r');
    usart_send_blocking(USART3, '\n');
}

void send_USART_bytes(const unsigned char* in, int n)
{
    int i;
    for(i = 0; i < n; i++) {
        usart_send_blocking(USART3, in[i]);
    }
}

void recv_USART_bytes(unsigned char* out, int n)
{
    int i;
    for(i = 0; i < n; i++) {
        out[i] = usart_recv_blocking(USART3);
    }
}

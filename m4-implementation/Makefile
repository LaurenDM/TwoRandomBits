.PHONY: all clean lib

PREFIX	?= arm-none-eabi
CC		= $(PREFIX)-gcc
LD		= $(PREFIX)-gcc
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
GDB		= $(PREFIX)-gdb

OPENCM3DIR ?= libopencm3
COMMONDIR  ?= common

all: lib aes_128_ctr_bs_masked_2br.bin analysis.bin nisttestvector.bin analysis1sbox.bin

CFLAGS   += -DSTM32F4
LDSCRIPT = $(COMMONDIR)/stm32f407x6.ld
LDFLAGS  += -L$(OPENCM3DIR)/lib -lopencm3_stm32f4
OBJS     += $(COMMONDIR)/stm32f4_wrapper.o
OBJS     += aes_128_ctr_bs_masked_2br.s
#OBJS     += aes_128_ctr_bs_masked.s
#OBJS     += aes_128_ctr_bs_masked_2br_submitted.s
#OBJS     += aes_128_ctr_bs_masked_2br_reseteverywhere.s
#OBJS     += 1sbox.s
OBJS     += sbox_regclr_memflush_aluflush.s

ARCH_FLAGS = -mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16
CFLAGS     += -O3 \
		   -Wall -Wextra -Wimplicit-function-declaration \
		   -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes \
		   -Wundef -Wshadow \
		   -I$(OPENCM3DIR)/include \
		   -fno-common $(ARCH_FLAGS) -MD
LDFLAGS    += --static -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections,--no-print-gc-sections \
		   $(ARCH_FLAGS)

lib:
	@if [ 0 -eq "`ls -A $(OPENCM3DIR) 2>/dev/null | wc -l`" ]; then \
		printf >&2 "Error: libopencm3 is not initialized\n"; \
		printf >&2 "Run 'git submodule update --init' before running make\n"; \
		exit 1; \
	fi
	make -C $(OPENCM3DIR)

%.bin: %.elf
	$(OBJCOPY) -Obinary $^ $@

%.elf: %.o $(OBJS) $(LDSCRIPT)
	$(LD) -o $@ $< $(OBJS) $(LDFLAGS)

%.o: %.c 
	$(CC) $(CFLAGS) -o $@ -c $^

clean:
	rm -f *.o *.d *.elf *.bin

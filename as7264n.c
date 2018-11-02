/* @file as7264n.c
 *
 * @brief AS7264N Color Sensor driver. Multiple AS7264N on a TCA9548A i2c Mux.
 * */

#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>

#define MUX_ADDR 0x70  //i2c muxer address 0b1110000r
#define SENS_ADDR 0x49 //col sens address  0b1001001r

int file;
char *filename = "/dev/i2c-2";
if ((file = open(filename, O_RDWR)) < 0) {
        /* ERROR HANDLING: you can check errno to see what went wrong */
        perror("Failed to open the i2c bus");
            exit(1);

}

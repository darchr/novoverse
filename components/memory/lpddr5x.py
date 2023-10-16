from m5.objects import DRAMInterface


class LPDDR5X(DRAMInterface):
    device_size = "8GiB"
    device_rowbuffer_size = "1KiB"

    beats_per_clock = 8
    device_bus_width = 16
    burst_length = 32
    # 8533MHz DDR, I used 8000MHz DDR -> 250ps clock period
    tCK = "250ps"
    # 8 * 250ps
    # To calculate tBURST I used (burst_length/beats_per_clock) * tCK
    tBURST = "1ns"
    # No pseudo-channeling so tBURST = tBURST_MIN = tBURST_MAX
    tBURST_MIN = "1ns"
    tBURST_MAX = "1ns"

    # Guess
    devices_per_rank = 1
    # Looking at nvidia grace white paper there are 2 devices for each channel
    ranks_per_channel = 2
    # Anandtech: banks per channel = 16
    banks_per_rank = 8
    # Guess, makes most sense
    bank_groups_per_rank = 4

    activation_limit = 4
    # 40 cycles
    tXAW = "10ns"

    # 48 cycles
    tRCD = "12ns"
    tCL = "12ns"
    tRP = "12ns"

    # 96 cycles
    tRAS = "24ns"

    # 8 cycles
    tRRD = "1ns"

    # 16 cycles
    tRRD_L = "2ns"
    tCCD_L = "2ns"

    # 2 cycles
    tCS = "500ps"
    tRTW = "500ps"

    tRTP = "7.5ns"
    tWTR = "7.5ns"
    tWR = "15ns"

    tRFC = "260ns"
    tREFI = "7.8us"

    tXP = "6ns"
    tXS = "270ns"

    # Current values from datasheet Die Rev E,J
    IDD0 = "55mA"
    IDD2N = "32mA"
    IDD3N = "38mA"
    IDD4W = "125mA"
    IDD4R = "157mA"
    IDD5 = "235mA"
    IDD3P1 = "38mA"
    IDD2P1 = "32mA"
    IDD6 = "20mA"
    VDD = "1.5V"

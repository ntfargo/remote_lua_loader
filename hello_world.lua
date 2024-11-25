function main()
    local pid = syscall.getpid():tonumber()
    
    syscall.resolve({
        getppid = 39,
    })
    local ppid = syscall.getppid():tonumber()

    local bases = {
        eboot = eboot_base,
        libc = libc_base,
        libkernel = libkernel_base
    }
 
    print("\n=== System Information ===")
    printf("Platform: %s (%s)", PLATFORM, FW_VERSION)
    printf("Process ID: %d", pid)
    printf("Parent Process ID: %d", ppid)
 
    print("\n=== Base Addresses ===")
    printf("eboot     @ %s", hex(bases.eboot))
    printf("libc      @ %s", hex(bases.libc))
    printf("libkernel @ %s", hex(bases.libkernel))
end

main()
"""
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <sys/syscall.h>
#include <linux/audit.h>
"""

blacklist = [
    "execve",
    "execveat",
]

code = """
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 0, [KILL]),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
  BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, 0x40000000 , 0, 1),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0xffffffff , 0, [KILL]),
""".strip("\n").splitlines()

for sys in blacklist:
    code.append(f"  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_{sys}, [KILL], 0),")

code += """
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
""".strip("\n").splitlines()

kill = len(code)-1

for i, line in enumerate(code):
    if not "[KILL]" in line:
        continue
    code[i] = line.replace("[KILL]", str(kill-(i+1)))

print("struct sock_filter sock_filter[] = {")
print("\n".join(code))
print("};")
print("""
struct sock_fprog prog = {
  .len = sizeof(sock_filter) / sizeof(sock_filter[0]),
  .filter = sock_filter,
};

void load_seccomp() {
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(EXIT_FAILURE);
  }
  if(syscall(__NR_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog) < 0) {
    perror("seccomp(SECCOMP_SET_MODE_FILTER)");
    exit(EXIT_FAILURE);
  }
}
""")
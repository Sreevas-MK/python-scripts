import subprocess, os

date=subprocess.getoutput("date")
print(f"-- System report ({date}) --\n")

out = subprocess.check_output(["uptime", "-p"]).decode().strip()
print(f"System is {out}")

cpu = os.getloadavg()
print(f"Load averages are: {cpu[0]}, {cpu[1]}, {cpu[2]}\n")

mem_sorted = subprocess.getoutput("free -h | grep -i mem").split()
print(f"Memory used is: {mem_sorted[2]} out of {mem_sorted[1]}")
print(f"Memory use %: {(float(mem_sorted[2][:-2])/float(mem_sorted[1][:-2])*100):.2f}")
print(f"Available memory is:  {mem_sorted[6]}")

print("\n-- Disk usage report --\n")
out = subprocess.getoutput("df -h")
line = out.split("\n")[1:]

usage_list=[]
for x in line:
    parts = x.split()

    try:
        z = int(parts[4].replace("%",""))
        usage_list.append((z, parts[0], parts[2], parts[1]))
    except ValueError:
        z = 0
        usage_list.append((z, parts[0], parts[2], parts[1]))

usage_list.sort(reverse=True)

for a,s,d,f in usage_list:
    print(f"{s} have Disk usage of {d}/{f} - {a}%")

print()

highest = usage_list[0]
print(f"Highest Disk usage is for: {highest[1]} - {highest[2]}/{highest[3]} with {highest[0]}%")


print("\n-- Inode usage report ---\n")

output = subprocess.getoutput("df -i")
lines = output.split("\n")[1:]

inode_list=[]
for x in lines:
    parts = x.split()

    try:
        z = int(parts[4].replace("%",""))
        inode_list.append((z, parts[0], parts[2], parts[1]))
    except ValueError:
        z = 0
        inode_list.append((z, parts[0], parts[2], parts[1]))

inode_list.sort(reverse=True)

for a,s,d,f in inode_list:
    print(f"{s} have inode usage of {d}/{f} - {a}%")

print()

highest_inodes = inode_list[0]
print(f"Highest Inode usage is for: {highest_inodes[1]} - {highest_inodes[2]}/{highest_inodes[3]} with {highest_inodes[0]}%")

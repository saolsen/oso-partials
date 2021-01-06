# new builtins, they look like rules but they aint they return values
# yeah it's confusing, sorry.
# sqrt(f)
# min(a,b)
# max(a,b)
# sign(f)

?= 1 = min(1.0,2.0);
?= 2 = max(1.0,2.0);

absv(x,y,z,ax,ay,az) if
    ax = abs(x) and
    ay = abs(y) and
    az = abs(z);

minv(ax,ay,az,bx,by,bz,mx,my,mz) if
    mx = min(ax,bx) and
    my = min(ay,by) and
    mz = min(az,bz);

maxv(ax,ay,az,bx,by,bz,mx,my,mz) if
    mx = max(ax,bx) and
    my = max(ay,by) and
    mz = max(az,bz);

?= maxv(
    1.0,3.0,1.0,
    4.0,-2.0,1.0,
    4.0,3.0,1.0);

sub(ax,ay,az,bx,by,bz,rx,ry,rz) if
    rx = ax - bx and
    ry = ay - by and
    rz = az - bz;

len(x, y, z, ans) if ans = sqrt(x*x + y*y + z*z);

box(x,y,z,bx,by,bz,ans) if
    absv(x,y,z,ax,ay,az) and
    sub(ax,ay,az,bx,by,bz,qx,qy,qz) and
    maxv(qx,qy,qz,0.0,0.0,0.0,mqx,mqy,mqz) and
    len(mqx,mqy,mqz,l) and
    m = max(qy,qz) and
    mm = max(qx,m) and
    mmm = min(mm,0.0) and
    ans = l + mmm;

#sdf(x,y,z,ans) if box(x,y,z,1.0,1.0,1.0,ans);

sphere(x, y, z, cx, cy, cz, radius, ans) if
    ox = x - cx and
    oy = y - cy and
    oz = z - cz and
    len(ox,oy,oz, l) and
    ans = l - radius;

# doublesphere(x, y, z, cx, cy, cz, radius, ans) if
#     sub(x,y,z,cx,cy,cz,ox,oy,oz) and
#     # ox = x - cx and
#     # oy = y - cy and
#     # oz = z - cz and
#     len(ox,oy,oz, l) and
#     ans_a = l - radius and
#     sub(x,y,z,cx+1.0,cy+1.0,cz+1.0,obx,oby,obz) and
#     # obx = x - cx+1.0 and
#     # oby = y - cy+1.0 and
#     # obz = z - cz+1.0 and
#     len(obx,oby,obz, lb) and
#     ans_b = lb - radius and
#     ans = min(ans_a, ans_b);

# sdf(x,y,z,ans) if doublesphere(x,y,z,1.0,1.0,0.0,1.25,ans);

# sdf(x,y,z,ans) if
#     ox = x - 1.0 and
#     oy = y - 1.0 and
#     oz = z - 1.0 and
#     len(ox,oy,oz, l) and
#     #l = sqrt(ox*ox + oy*oy + oz*oz) and
#     obx = x - 2.0 and
#     oby = y - 2.0 and
#     obz = z - 2.0 and
#     #lb = sqrt(obx*obx + oby*oby + obz*obz) and
#     len(obx,oby,obz, lb) and
#     ans = l + lb;

difference(a,b,ans) if ans = max(a, b * -1.0);
union(a,b,ans) if ans = min(a, b);

# sdf(x,y,z,ans) if
#     sphere(x,y,z,1.0,1.0,0.0,1.25,ans_a) and
#     print(ans_a) and
#     sphere(x,y,z,1.0,1.0,0.0,1.25,ans_b) and
#     print(ans_b) and
#     ans = ans_a + ans_b;
    #difference(ans_a, ans_b, ans);
# sdf(x,y,z,ans) if  box(x,y,z,1.0,1.0,1.0,ans);

# sdf(x,y,z,ans) if
#     sphere(x,y,z,0.0,0.0,0.0,1.25,s_ans) and
#     sphere(x,y,z,0.0,1.0,0.0,1.25,b_ans) and
#     ans = min(s_ans, b_ans);
    #box(x,y,z,1.0,1.0,1.0,b_ans) and
    #ans = s_ans;
    #ans = max(s_ans, b_ans * -1.0);
    #difference(s_ans, b_ans, ans);

sdf(x,y,z,ans) if sphere(x,y,z,1.0,1.0,0.0,1.25,ans);
# sdf(x,y,z,ans) if sphere(x,y,z,-1.0,1.0,0.0,1.25,ans);

# sdf(x,y,z,ans) if x < 0.0 and ans = 1.0;
# sdf(x,y,z,ans) if x >= 0.0 and ans = 2.0;

# NOTE: Don't cut lol

# f(x,y,z,ans_f) if
#     ans_f = min(x, y);

# g(x,y,z,ans_g) if
#     ans_g = min(x, y*-1.0);

# sdf(x,y,z,ans) if
#     f(x,y,z,a) and g(x,y,z,b) and ans = a + b;
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

box(x,y,z,bx,by,bz,ans) if
    absv(x,y,z,ax,ay,az) and
    sub(ax,ay,az,bx,by,bz,qx,qy,qz) and
    maxv(qx,qy,qz,0.0,0.0,0.0,mqx,mqy,mqz) and
    len(mqx,mqy,mqz,l) and
    m = max(qy,qz) and
    mm = max(qx,m) and
    mmm = min(mm,0.0) and
    ans = l + mmm;

sdf(x,y,z,ans) if box(x,y,z,1.0,1.0,1.0,ans);

# The sdf function returns the distance from a point x,y,z to a surface.
len(x, y, z, ans) if ans = sqrt(x*x + y*y + z*z);

sphere(x, y, z, cx, cy, cz, radius, ans) if
    sub(x,y,z,cx,cy,cz,ox,oy,oz) and
    len(ox,oy,oz, l) and
    ans = l - radius;

#sdf(x,y,z,ans) if sphere(x,y,z,1.0,1.0,0.0,1.25,ans);
#sdf(x,y,z,ans) if sphere(x,y,z,-1.0,1.0,0.0,1.25,ans);

# sdf(x,y,z,ans) if x < 0.0 and ans = 1.0;
# sdf(x,y,z,ans) if x >= 0.0 and ans = 2.0;

# NOTE: Don't cut lol
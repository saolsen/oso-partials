# new builtins, they look like rules but they aint they return values
# yeah it's confusing, sorry.
# sqrt(f)
# min(a,b)
# max(a,b)
# sign(f)

# abs is a glsl builtin and could use that
abs(x,ax) if x >= 0.0 and ax = x;
abs(x,ax) if x < 0.0 and ax = x * -1.0;
abs(x,y,z,ax,ay,az) if
    abs(x,ax) and
    abs(y,ay) and
    abs(z,az);

min(x,y,ans) if x <= y and ans = x;
min(x,y,ans) if x > y and ans = y;
min(ax,ay,az,bx,by,bz,mx,my,mz) if
    min(ax,bx,mx) and
    min(ay,by,my) and
    min(az,bz,mz);

max(x,y,ans) if x >= y and ans = x;
max(x,y,ans) if x < y and ans = y;
max(ax,ay,az,bx,by,bz,mx,my,mz) if
    max(ax,bx,mx) and
    max(ay,by,my) and
    max(az,bz,mz);

?= max(
    1,3,1,
    4,-2,1,
    4,3,1);

sub(ax,ay,az,bx,by,bz,rx,ry,rz) if
    rx = ax - bx and
    ry = ay - by and
    rz = az - bz;

box(x,y,z,bx,by,bz,ans) if
    abs(x,y,z,ax,ay,az) and
    sub(ax,ay,az,bx,by,bz,qx,qy,qz) and
    max(qx,qy,qz,0.0,0.0,0.0,mqx,mqy,mqz) and
    len(mqx,mqy,mqz,l) and
    max(qy,qz,m) and
    max(qx,m,mm) and
    min(mm,0.0,mmm) and
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
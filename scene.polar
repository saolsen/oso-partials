# The sdf function returns the distance from a point x,y,z to a surface.
len(x, y, z, ans) if ans = sqrt(x*x + y*y + z*z);

# A unit sphere
sdf(x, y, z, ans) if
    len(x,y,z,len) and
    ans = len - 1.0;
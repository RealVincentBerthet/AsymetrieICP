function affiche_plan(normale,distance, couleur)

p0 = distance*normale;
v1 = cross(normale,rand(size(normale))); v1 = v1/norm(v1);
v2 = cross(normale,v1);
plane = [p0 v1 v2];

if (nargin<3)
    drawPlane3d(plane);
else
    drawPlane3d(plane,couleur);
end
end

function varargout = drawPlane3d(plane, varargin)
%DRAWPLANE3D Draw a plane clipped in the current window
%
%   drawPlane3d(plane)
%   plane = [x0 y0 z0  dx1 dy1 dz1  dx2 dy2 dz2];
%
%   See also
%   planes3d, createPlane
%
%   Example
%   p0 = [1 2 3];
%   v1 = [1 0 1];
%   v2 = [0 -1 1];
%   plane = [p0 v1 v2];
%   axis([-10 10 -10 10 -10 10]);
%   drawPlane3d(plane)
%   drawLine3d([p0 v1])
%   drawLine3d([p0 v2])
%   set(gcf, 'renderer', 'zbuffer');
%
%   ---------
%   author : David Legland
%   INRA - TPV URPOI - BIA IMASTE
%   created the 17/02/2005.
%

%   HISTORY
%   2008-10-30 replace intersectPlaneLine by intersectLinePlane, add doc
%   2010-10-04 fix a bug for planes touching box by one corner

param = 'm';
if ~isempty(varargin)
    param = varargin{:};
end

lim = get(gca, 'xlim');
xmin = lim(1);
xmax = lim(2);
lim = get(gca, 'ylim');
ymin = lim(1);
ymax = lim(2);
lim = get(gca, 'zlim');
zmin = lim(1);
zmax = lim(2);


% line corresponding to cube edges
lineX00 = [xmin ymin zmin 1 0 0];
lineX01 = [xmin ymin zmax 1 0 0];
lineX10 = [xmin ymax zmin 1 0 0];
lineX11 = [xmin ymax zmax 1 0 0];

lineY00 = [xmin ymin zmin 0 1 0];
lineY01 = [xmin ymin zmax 0 1 0];
lineY10 = [xmax ymin zmin 0 1 0];
lineY11 = [xmax ymin zmax 0 1 0];

lineZ00 = [xmin ymin zmin 0 0 1];
lineZ01 = [xmin ymax zmin 0 0 1];
lineZ10 = [xmax ymin zmin 0 0 1];
lineZ11 = [xmax ymax zmin 0 0 1];


% compute intersection points with each plane
piX00 = intersectLinePlane(lineX00, plane);
piX01 = intersectLinePlane(lineX01, plane);
piX10 = intersectLinePlane(lineX10, plane);
piX11 = intersectLinePlane(lineX11, plane);
piY00 = intersectLinePlane(lineY00, plane);
piY01 = intersectLinePlane(lineY01, plane);
piY10 = intersectLinePlane(lineY10, plane);
piY11 = intersectLinePlane(lineY11, plane);
piZ00 = intersectLinePlane(lineZ00, plane);
piZ01 = intersectLinePlane(lineZ01, plane);
piZ10 = intersectLinePlane(lineZ10, plane);
piZ11 = intersectLinePlane(lineZ11, plane);

% concatenate points into one array
points = [...
    piX00;piX01;piX10;piX11; ...
    piY00;piY01;piY10;piY11; ...
    piZ00;piZ01;piZ10;piZ11;];

% check validity: keep only points inside window
ac = 1e-14;
vx = points(:,1)>=xmin-ac & points(:,1)<=xmax+ac;
vy = points(:,2)>=ymin-ac & points(:,2)<=ymax+ac;
vz = points(:,3)>=zmin-ac & points(:,3)<=zmax+ac;
valid = vx & vy & vz;
pts = unique(points(valid, :), 'rows');

% If there is no intersection point, escape.
if size(pts, 1)<3
    disp('plane is outside the drawing window');
    return;
end

% the two spanning lines of the plane
d1 = plane(:, [1:3 4:6]);
d2 = plane(:, [1:3 7:9]);

% position of intersection points in plane coordinates
u1 = linePosition3d(pts, d1);
u2 = linePosition3d(pts, d2);

% reorder vertices in the correct order
ind = convhull(u1, u2);
ind = ind(1:end-1);

% draw the patch
h = patch(pts(ind, 1), pts(ind, 2), pts(ind, 3), param);
alpha(h,.9);
% return handle to plane if needed
if nargout>0
    varargout{1}=h;
end

end


function point = intersectLinePlane(line, plane)
%INTERSECTLINEPLANE return intersection between a plane and a line
%
%   PT = intersectLinePlane(LINE, PLANE)%
%   Returns the intersection point of the given line and the given plane.
%   PLANE : [x0 y0 z0 dx1 dy1 dz1 dx2 dy2 dz2]
%   LINE :  [x0 y0 z0 dx dy dz]
%   PT :    [xi yi zi]
%   If LINE and PLANE are parallel, return [NaN NaN NaN].
%   If LINE (or PLANE) is a matrix with 6 (or 9) columns and N rows, result
%   is an array of points with N rows and 3 columns.
%
%   See also:
%   lines3d, planes3d, points3d
%
%   ---------
%   author : David Legland
%   INRA - TPV URPOI - BIA IMASTE
%   created the 17/02/2005.
%

%   HISTORY
%   24/11/2005 add support for multiple input
%   23/06/2006 correction from Songbai Ji
%   14/12/2006 correction for parallel lines and plane normals
%   05/01/2007 fixup for parallel lines and plane normals
%   24/04/2007 rename as 'intersectLinePlane'
%   11/19/2010 Added bsxfun functionality for improved speed (Sven Holcombe)

%  Songbai Ji (6/23/2006). Bug fixed; also allow one plane, many lines;
% many planes one line; or N planes and N lines configuration in the input.

% unify sizes of data
plCnt = size(plane,1);
lnCnt = size(line,1);
if plCnt>1 && lnCnt>1 && plCnt~=lnCnt % N planes and M lines, not allowed for now.
    error('input size not correct, either one/many plane and many/one line, or same # of planes and lines!');
end

% plane normal
n = vectorCross3d(plane(:,4:6), plane(:,7:9));

% difference between origins of plane and line
dp = bsxfun(@minus, plane(:, 1:3), line(:, 1:3));

% relative position of intersection on line
t = sum(bsxfun(@times,n,dp),2)  ./  sum(bsxfun(@times,n,line(:,4:6)),2);

% compute coord of intersection point
point = bsxfun(@plus, line(:,1:3),  bsxfun(@times, [t t t], line(:,4:6)));

% set indices of line and plane which are parallel to NaN
par = abs( sum(bsxfun(@times, n, line(:,4:6)), 2) ) < 1e-14;
point(par,:) = NaN;

end

function d = linePosition3d(point, line)
%LINEPOSITION3D Return the position of a 3D point on a 3D line
%
%   L = linePosition3d(POINT, LINE)
%   compute position of point POINT on the line LINE, relative to origin
%   point and direction vector of the line.
%   LINE has the form [x0 y0 z0 dx dy dy],
%   POINT has the form [x y z], and is assumed to belong to line.
%   If POINT does not belong to LINE, the position of its orthogonal
%   projection is computed instead.
%
%   L = linePosition3d(POINT, LINES)
%   if LINES is an array of NL lines, return NL positions, corresponding to
%   each line.
%
%   L = linePosition3d(POINTS, LINE)
%   if POINTS is an array of NP points, return NP positions, corresponding
%   to each point.
%
%   See also:
%   lines3d, points3d, createLine3d
%
%   ---------
%   author : David Legland
%   INRA - TPV URPOI - BIA IMASTE
%   created the 17/02/2005.
%

%   HISTORY
%   05/01/2007 update doc
%   28/10/2010 change to bsxfun calculation for arbitrary input sizes
%       (Thanks to Sven Holcombe)

% vector from line origin to point
dp = bsxfun(@minus, point, line(:,1:3));

% direction vector of the line
dl = line(:, 4:6);

% compute position using dot product normalized with norm of line vector.
d = bsxfun(@rdivide, sum(bsxfun(@times, dp, dl), 2), sum(dl.^2, 2));
end

function c = vectorCross3d(a,b)
%VECTORCROSS  Vector cross product faster than inbuilt MATLAB cross.
%
%   C = VECTORCROSS(A,B) returns the cross product of the vectors A and B.
%   That is, C = A x B.
%   A and B must be Nx3 element vectors. If either A or B is a 1x3 element
%   vector, C will have the size of the other input and will be the
%   concatenation of each row's cross product.
%
%   Class support for inputs A,B:
%      float: double, single
%
%   See also DOT.

%   Sven Holcombe

% needed_colons = max([3, length(size(a)), length(size(b))]) - 3;
% tmp_colon = {':'};
% clnSet = tmp_colon(ones(1, needed_colons));
%
% c = bsxfun(@times, a(:,[2 3 1],clnSet{:}), b(:,[3 1 2],clnSet{:})) - ...
%     bsxfun(@times, b(:,[2 3 1],clnSet{:}), a(:,[3 1 2],clnSet{:}));

sza = size(a);
szb = size(b);

% Initialise c to the size of a or b, whichever has more dimensions. If
% they have the same dimensions, initialise to the larger of the two
switch sign(numel(sza) - numel(szb))
    case 1
        c = zeros(sza);
    case -1
        c = zeros(szb);
    otherwise
        c = zeros(max(sza,szb));
end

c(:) =  bsxfun(@times, a(:,[2 3 1],:), b(:,[3 1 2],:)) - ...
    bsxfun(@times, b(:,[2 3 1],:), a(:,[3 1 2],:));
end
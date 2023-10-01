close all
clear variables
imleft = imread('pictures\left.jpg');
imright = imread('pictures\right.jpg');
imleft = imresize(imleft,1/3);
imright = imresize(imright,1/3);
nrow =size(imleft,1);
ncol =size(imleft,2);

% determine the points interactively
[pL,pR] = cpselect(imleft,imright,'Wait',true);

figure(1); imshow(imleft); title('left');
figure(2); imshow(imright); title('right');
figure(1); hold on; plot(pL(:,1),pL(:,2),'rx');
figure(2); hold on; plot(pR(:,1),pR(:,2),'rx');

% find the projective transform
Htform = cp2tform(pR,pL,'projective');


%% step 1: transform the right image
% calculate the needed output space by finding out where the corners of the
% right image will be mapped to
Corners_im = [1    ncol    ncol    1;
              1    1       nrow    nrow];
[Cx,Cy] = tformfwd(Htform,Corners_im(1,:),Corners_im(2,:));
xim = [min([Cx 1]) max([Cx ncol])];
yim = [min([Cy 1]) max([Cy nrow])];

imstitchR = imtransform(imright,Htform,'XData',xim,'YData',yim,'XYscale',1);

%% step 2: transform the left image
Tunit = maketform('affine',[1 0 0; 0 1 0; 0 0 1]);
imstitchL = imtransform(imleft,Tunit,'XData',xim,'YData',yim,'XYscale',1);

%% step 3: now stitch them:
imstitchL(imstitchL==0) = imstitchR((imstitchL==0));
% or
imstitchL = max(imstitchL,imstitchR);
imtool(imstitchL);

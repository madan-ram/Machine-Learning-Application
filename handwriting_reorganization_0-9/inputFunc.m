function []=inputFunc(name)
    load('all_theta');
    img=mat2gray(rgb2gray(imread(name)));
    img1=img(:)';
    predictOneVsAll(all_theta,img1);
end
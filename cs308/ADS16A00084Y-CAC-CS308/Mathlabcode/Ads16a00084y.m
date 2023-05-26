%image processing using weiner filtering
close all
clear
clc

%reading input image
A = imread('py.png');
%A = imread('wallpaperflare.com_wallpaper.jpg');
A = double (rgb2gray(A));
[M, N] = size (A);

%degradation function
h = ones (5,5)/25;
%transformation to frequency domain
Freq_a = fft2(A);
Freq_h = fft2(h,M,N);

%degraded image in spatial domain
B = real(ifft2(Freq_h.* Freq_a))+ 25*randn(M,N);

%Wiener filtering
Freq_b = fft2(B);
pow_b = abs(Freq_b).^2/(M*N);
sigma = 50;
gamma = 1;
alpha = 1;
sFreq_h = Freq_h.*(abs(Freq_h)>0)+1/gamma*(abs(Freq_h)==0);
iFreq_h = 1./sFreq_h;
inFreq_h = iFreq_h.*(abs(Freq_h)*gamma>1)...
    +gamma*abs(sFreq_h).*iFreq_h.*(abs(sFreq_h)*gamma<=1);
pow_b = pow_b.*(pow_b>sigma^2)+sigma^2*(pow_b<=sigma^2);
Freq_g = iFreq_h.*(pow_b-sigma^2)./(pow_b-(1-alpha)*sigma^2);
Res_Freq_a = Freq_g.*Freq_b;

%restored image in spatial domain
Res_a = real(ifft2(Res_Freq_a));

%display of input /output images
imshow(uint8(A)), title('original image')
figure, imshow(uint8(B)), title('degraded image')
figure, imshow(uint8(Res_a)), title('Restored Image After Wiener filtering')

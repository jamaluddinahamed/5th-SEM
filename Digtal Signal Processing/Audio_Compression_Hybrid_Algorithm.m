%Project Name: Audio Compression Using Hybrid Algorithm
%MATLAB Code for Digital Signal Processing (EC550) Project (Event 2 and 4)
%Project submitted by 
%Shreyas K
%Jamal Uddin Ahamed

%Start of Program.
%This program is a combination of two algorithms (Hybrid Algorithm)
%First algorithm implementation (Micro Law of Compression).
%Used to remove unwanted bits from specific intervals of signal.
%Those bits whose presence or absence does not make a large difference are removed, Using this algorithm.

clc;
clear all;
close all;
file_name = input("Enter file to compress : ");
fileinfo = dir(file_name);
SIZE = fileinfo.bytes;
Size = SIZE/1024;
[x, Fs] = audioread(file_name);
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;
figure;
%Plot the input Audio Signal.
plot(t,x)
                  
[x,Fs] = audioread(file_name);
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;
wavelet='haar';
level=5; % input to wavedec
frame_size=2048; % input to wavedec

psychoacoustic='on ';
% Used for noise compression,
% A psychoacoustic (perceptual) model is used to analyze the input audio signal and determine relevant perceptual signal aspects
%most notably the signal's masking ability

wavelet_compression = 'on ';%The compression features of a given wavelet basis are primarily linked to the relative scarceness of the wavelet domain representation for the signal.
heavy_compression='off';
compander='on ';
quantization ='on ';

step=frame_size;
N=ceil(xlen/step);
%Rounding off numbers to nearest integer

Cchunks=0;
Lchunks=0;
Csize=0;
PERF0mean=0;
PERFL2mean=0;
n_avg=0;
n_max=0;
n_0=0;
n_vector=[];
for i=1:1:N
    if (i==N)
        frame=x([(step*(i-1)+1):length(x)]);
    else
        frame=x([(step*(i-1)+1):step*i]);
end

[C,L] = wavedec(frame,level,wavelet);
%wavedec performs a multilevel one-dimensional wavelet analysis using either a specific wavelet ('wname') in this case 'haar' or a specific wavelet decomposition filters 

if wavelet_compression=='on '
[thr,sorh,keepapp] = ddencmp('cmp','wv',frame);

    if heavy_compression == 'on '
        thr=thr*10^6;
    end
    [XC,CXC,LXC,PERF0,PERFL2] = wdencmp('gbl',C, L, wavelet,level,thr,sorh,keepapp);
    C=CXC;
    L=LXC;
    PERF0mean=PERF0mean + PERF0;
    PERFL2mean=PERFL2mean+PERFL2;
end

if psychoacoustic=='on '
    P=10.*log10((abs(fft(frame,length(frame)))).^2);
    Ptm=zeros(1,length(P));

        for k=1:1:length(P)
        if ((k<=1) | (k>=250))
        bool = 0;
        elseif ((P(k)<P(k-1)) | (P(k)<P(k+1))),
        bool = 0;
        elseif ((k>2) & (k<63)),
        bool = ((P(k)>(P(k-2)+7)) & (P(k)>(P(k+2)+7)));
        elseif ((k>=63) & (k<127)),
        bool = ((P(k)>(P(k-2)+7)) & (P(k)>(P(k+2)+7)) & (P(k)>(P(k-3)+7)) & (P(k)>(P(k+3)+7)));
        elseif ((k>=127) & (k<=256)),
        bool = ((P(k)>(P(k-2)+7)) & (P(k)>(P(k+2)+7)) & (P(k)>(P(k-3)+7)) & (P(k)>(P(k+3)+7)) & (P(k)>(P(k-4)+7)) & (P(k)>(P(k+4)+7)) &(P(k)>(P(k-5)+7)) & (P(k)>(P(k+5)+7)) & (P(k)>(P(k-6)+7)) &(P(k)>(P(k+6)+7)));
        else
        bool = 0;
        end
    if bool==1
        Ptm(k)=10*log10(10.^(0.1.*(P(k-1)))+10.^(0.1.*(P(k)))+10.^(0.1.*P(k+1)));
    end
end

sum_energy=0;

for k=1:1:length(Ptm)
    sum_energy=10.^(0.1.*(Ptm(k)))+sum_energy;
end
E=10*log10(sum_energy/(length(Ptm)));
SNR=max(P)-E;
n=ceil(SNR/6.02);
if n<=3
    n=4;
    n_0=n_0+1;
end
if n>=n_max
    n_max=n;
end
n_avg=n+n_avg;
n_vector=[n_vector n];
end

if compander=='on '
    Mu=255;
    C = compand(C,Mu,max(C),'mu/compressor');
end

if quantization=='on '
    if psychoacoustic=='off'
        n=8;
end
partition = [min(C):((max(C)-min(C))/2^n):max(C)];
codebook = [1 min(C):((max(C)-min(C))/2^n):max(C)];
[index,quant,distor] = quantiz(C,partition,codebook);

offset=0;
for j=1:1:N
    if C(j)==0
    offset=-quant(j);
    break;
end
end
quant=quant+offset;
C=quant;
end

Cchunks=[Cchunks C]; 
Lchunks=[Lchunks L];
Csize=[Csize length(C)];
Encoder = round((i/N)*100); %indicator of progess
end
Cchunks=Cchunks(2:length(Cchunks));

%wavwrite(Cchunks,Fs,bits,'output1.wav')
Csize=[Csize(2) Csize(N+1)];
Lsize=length(L);
Lchunks=[Lchunks(2:Lsize+1) Lchunks((N-1)*Lsize+1:length(Lchunks))];
PERF0mean=PERF0mean/N; %indicator
PERFL2mean=PERFL2mean/N;%indicator
n_avg=n_avg/N;%indicator
n_max;%indicator
end_of_encoder='done';
xdchunks=0;
for i=1:1:N;
    if i==N;
        Cframe=Cchunks([((Csize(1)*(i-1))+1):Csize(2)+(Csize(1)*(i-1))]);

        if compander=='on '
        if max(Cframe)==0
        else
            Cframe = compand(Cframe,Mu,max(Cframe),'mu/expander');
        end
    end
    xd = waverec(Cframe,Lchunks(Lsize+2:length(Lchunks)),wavelet);
    else
    Cframe=Cchunks([((Csize(1)*(i-1))+1):Csize(1)*i]);

    if compander=='on '
        if max(Cframe)==0
    else
        Cframe = compand(Cframe,Mu,max(Cframe),'mu/expander');
    end
    end
    xd = waverec(Cframe,Lchunks(1:Lsize),wavelet);
    end
    xdchunks=[xdchunks xd];
    Decoder = round((i/N)*100); %indicator of progess
end
xdchunks=xdchunks(2:length(xdchunks));

end_of_decoder='done';

audiowrite('AudioComp_Hybrid/Output/output1.wav',xdchunks,Fs);
end_of_writing_file='done';
[x,Fs] = audioread('AudioComp_Hybrid/Output/output1.wav');
fileinfo = dir('AudioComp_Hybrid/Output/output1.wav');
SIZE = fileinfo.bytes;
Size = SIZE/1024;

xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;

%
%
plot(t,xdchunks)
%
%

grid on

[y1,fs1]=audioread(file_name);
[y2,fs2]=audioread('AudioComp_Hybrid/Output/output1.wav');
[c1x,c1y]=size(y1);
[c2x,c2y]=size(y1);
if c1x ~= c2x
    disp('dimeonsions do not agree');
 else
 R=c1x;
 C=c1y;
  err = (sum(y1(2)-y2).^2)/(R*C);
 MSE=sqrt(err);
 MAXVAL=255;
  PSNR = 20*log10(MAXVAL/MSE); 
  MSE= num2str(MSE);
  if(MSE > 0)
  PSNR= num2str(PSNR);
  else
PSNR = 99;
end
fileinfo = dir(file_name);
SIZE = fileinfo.bytes;
Size = SIZE/1024;
fileinfo1 = dir('AudioComp_Hybrid/Output/output1.wav');
SIZE1 = fileinfo1.bytes;
Size1 = SIZE1/1024;

CompressionRatio = Size/Size1;
  disp("PSNR is : ");
  disp(PSNR)
  disp("MSE is : ");
  disp(MSE)
  disp("Compression Ratio is : ");
  disp(CompressionRatio)
end

% Second algorithm operating on same file
file_name = "output1.wav";
fileinfo = dir(file_name);
SIZE = fileinfo.bytes;
Size = SIZE/1024;
[x,Fs] = audioread(file_name);
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;
figure;
%
%
plot(t,x)
%
%

[Data,Fs] = audioread(file_name);

windowSize = 8192;
samplesHalf = windowSize / 2;
samplesQuarter = windowSize / 4;
samplesEighth = windowSize / 8;
DataCompressed2 = [];
DataCompressed4 = [];
DataCompressed8 = [];

for i=1:windowSize:length(Data)-windowSize
    windowDCT = dct(Data(i:i+windowSize-1));
    DataCompressed2(i:i+windowSize-1) = idct(windowDCT(1:samplesHalf), windowSize);
    DataCompressed4(i:i+windowSize-1) = idct(windowDCT(1:samplesQuarter), windowSize);
    DataCompressed8(i:i+windowSize-1) = idct(windowDCT(1:samplesEighth), windowSize);
end

audiowrite('AudioComp_Hybrid/Output/output3.wav',DataCompressed2,Fs)
[x,Fs] = audioread('AudioComp_Hybrid/Output/output3.wav');
fileinfo = dir('AudioComp_Hybrid/Output/output3.wav');
SIZE = fileinfo.bytes;
Size = SIZE/1024;
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;
figure;
%
%
plot(t,x)
%
%

grid on

audiowrite('AudioComp_Hybrid/Output/output4.wav',DataCompressed4,Fs)
[x,Fs] = audioread('AudioComp_Hybrid/Output/output4.wav');
fileinfo = dir('AudioComp_Hybrid/Output/output4.wav');
SIZE = fileinfo.bytes;
Size = SIZE/1024;
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;
figure;
%
%
plot(t,x)
%
%

grid on

audiowrite('AudioComp_Hybrid/Output/output5.wav',DataCompressed8,Fs)
[x,Fs] = audioread('AudioComp_Hybrid/Output/output5.wav');
fileinfo = dir('AudioComp_Hybrid/Output/output5.wav');
SIZE = fileinfo.bytes;
Size = SIZE/1024;
xlen=length(x);
t=0:1/Fs:(length(x)-1)/Fs;

figure;
%
%
plot(t,x)
%
%

grid on


[y1,fs1]=audioread(file_name);
[y2,fs2]=audioread('AudioComp_Hybrid/Output/output3.wav');
[c1x,c1y]=size(y1);
[c2x,c2y]=size(y1);
if c1x ~= c2x
    disp('dimeonsions do not agree');
 else
 R=c1x;
 C=c1y;
  err = (sum(y1(2)-y2).^2)/(R*C);
 MSE=sqrt(err);
 MAXVAL=255;
   PSNR = 20*log10(MAXVAL/MSE); 
  MSE= num2str(MSE);
if(MSE > 0)
  PSNR= num2str(PSNR);
   else
PSNR = 99;
end
fileinfo = dir(file_name);
SIZE = fileinfo.bytes;
Size = SIZE/1024;
fileinfo1 = dir('AudioComp_Hybrid/Output/output3.wav');
SIZE1 = fileinfo1.bytes;
Size1 = SIZE1/1024;

CompressionRatio = Size/Size1;
end


[A,fs]=audioread(file_name);

%Sender
C=[];
A=A';
for i=512:512:numel(A)
    B=dct(A(i-511:i));
    C=[C, B(1:128)];
end

%Reciever
A2=[];
for i=128:128:numel(C)
    S=[C(i-127:i),zeros(1,384)];
    S=idct(S);
    A2=[A2,S];
end

% Evaluation
dis=numel(A)-numel(A2);
A2=[A2,zeros(1,dis)];
PSNR=psnr(A2,A)
%MSError=mse(A2,A)
SNR=snr(A2,A)

% plot
figure,
plot(A);
hold on
plot(A2,'r')
plot((A2-A),'y')
legend('Original' , 'Recieved','Difference')
title('Audio Compression By DCT');
xlabel('Samples');
ylabel('Amp.');
grid();
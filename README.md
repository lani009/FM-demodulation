# RTL-SDR과 Numpy, Scipy를 이용한 FM 라디오 복조

## What is RTL-SDR?

RTL-SDR은 RTL2832칩셋을 이용해 저렴한 가격으로 만들어진 SDR 장비를 말한다.
SDR을 활용하면 컴퓨터 CPU의 무궁무진한 범용 컴퓨팅 능력을 이용하여,
내가 원하는 방식으로 무선 신호를 처리하게끔 소프트웨어를 개발할 수 있다.

가령, 8PSK 디지털통신을 디코딩한다고 가정해보자.
RTL-SDR 장비와 안테나만 있다면 모든 준비는 끝났다.
8PSK를 디코딩 할 수 있도록 소프트웨어를 직접 개발하면 된다.

이 레포지터리에서는 FM 라디오신호를 복조할 수 있는 소프트웨어를 개발하고자 한다.
실제 FM 라디오의 전자회로를 소프트웨어적으로 구현할 수 있게끔 Numpy와 Scipy를 이용하여
필터와 다운컨버터 등 여러가지를 개발해 볼 것이다.

## Source codes

- main SRC

    [FM Demod](FM%20radio%20demodulator.ipynb)

- fft test

    [FFT Test](sdr_fft.ipynb)

- realtime fm radio

    [RealtimeRadio](RealtimeRadio.py)

- experiment result - radio audio

    [ad1](wbfm.wav)

    [ad2](wbfm_test.wav)


## Figure

### Specgram of raw input

![x1](img/FM%20radio%20demodulator_2_0.png)


### Specgram of shifted in frequency domain

![x2](img/FM%20radio%20demodulator_3_0.png)
    

### Specgram of Filtered signal
```python
f_bw = 200000

lpf = signal.remez(64, [0, f_bw, f_bw+(Rs/2-f_bw)/4, Rs/2], [1, 0], fs=Rs)
w, h = signal.freqz(lpf, 1, worN=2000)
x3 = signal.lfilter(lpf, 1.0, x2)

plt.specgram(x3, NFFT=2048, Fs=Rs)
plt.title("x3")
plt.ylim(-Rs/2, Rs/2)
plt.xlim(0, len(x3)/Rs)
plt.ticklabel_format(style='plain', axis='y')

ax2 = plt.twiny()
ax2.plot(20*np.log10(np.abs(h)), 0.5*Rs*w/np.pi, 'm')
ax2.set_xlabel('Gain (dB)')
ax2.set_xlim(-120, 5)

ax2 = plt.twiny()
ax2.plot(20*np.log10(np.abs(h)), -0.5*Rs*w/np.pi, 'm')
ax2.set_xlim(-120, 5)

plt.savefig('./figure/x3.png', dpi=200, facecolor='#eeeeee')
plt.show()

plt.plot(0.5*Rs*w/np.pi, 20*np.log10(np.abs(h)))
plt.ylim(-100, 3)
plt.xlim(0, Rs/2)
plt.grid(True)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('Low pass filter')
plt.savefig('./figure/lpf.png', dpi=200, facecolor='#eeeeee')
plt.show()
```

![png](img/FM%20radio%20demodulator_4_0.png)

![png](img/FM%20radio%20demodulator_4_1.png)
    


### Decimated

![png](img/FM%20radio%20demodulator_5_0.png)
    

### Signal Constellation

![png](img/FM%20radio%20demodulator_5_1.png)


### PSD in frequency

![png](img/FM%20radio%20demodulator_6_0.png)

## Conclusion

RTL-SDR 장비를 활용해 FM 신호를 복조하는 소프트웨어를 개발해보았다.
더욱 최적화 할 수 있는 방법이 있으나, 실제 라디오에서 사용하는 슬로프 디텍터 등 하드웨어를 모사하기 위해서
소프트웨어도 이와 유사하게 개발하였다.

이처럼 Numpy와 Scipy를 활용하면, IQ 샘플링된 무선 신호를 내가 원하는 대로 조작할 수 있음을 보였다.
Scipy 라이브러리로 내가 원하는 필터를 설계하거나, 다운컨버팅 등 다양한 연산을 수행할 수 있고,
Numpy를 활용해 FFT를 하는 등의 연산을 수행할 수 있었다.

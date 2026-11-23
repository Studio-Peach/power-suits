#!/usr/bin/env python3
"""Generates Power Suits' custom mono Ogg Vorbis sound effects (44.1 kHz, seamless loops).

Run: uv run --with numpy --with soundfile python3 tools/make-sounds.py

Why mono Ogg Vorbis: Minecraft / OpenAL only applies 3D positional attenuation to mono .ogg files
(stereo sounds play at full volume everywhere in the world). Every periodic oscillator runs at an
exact multiple of 1/T Hz and all noise bands are shaped circularly in the FFT domain so loops wrap
with zero click or seam.
"""
import os
import numpy as np
import soundfile as sf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'power_suits', 'sounds')
SR = 44100


def _circ_band_noise(rng, n, freqs, f_lo, f_hi, order=2.0):
    """Circularly band-passed noise (100% seamless across sample n-1 -> 0)."""
    x = rng.standard_normal(n)
    X = np.fft.rfft(x)
    hp = 1.0 / np.sqrt(1.0 + (f_lo / np.maximum(freqs, 1e-6)) ** (2 * order))
    lp = 1.0 / np.sqrt(1.0 + (freqs / f_hi) ** (2 * order))
    mask = hp * lp
    mask[0] = 0.0
    y = np.fft.irfft(X * mask, n=n)
    return y / (np.std(y) + 1e-9)


def _circ_eq(x, freqs, f_lo=45.0, f_hi=4200.0):
    X = np.fft.rfft(x)
    hp = 1.0 / np.sqrt(1.0 + (f_lo / np.maximum(freqs, 1e-6)) ** 4)
    lp = 1.0 / np.sqrt(1.0 + (freqs / f_hi) ** 4)
    X *= hp * lp
    X[0] = 0.0
    return np.fft.irfft(X, n=len(x))


def _harm_motor(t, f0, weights, lfo_f, lfo_depth, rng):
    ph = 2 * np.pi * f0 * t + (lfo_depth / lfo_f) * np.sin(2 * np.pi * lfo_f * t)
    y = np.zeros_like(t)
    for k, w in enumerate(weights, start=1):
        y += w * np.sin(k * ph + rng.uniform(0, 2 * np.pi))
    return y


def _pulse_train(t, rate_hz, sharpness):
    return (0.5 * (1.0 + np.cos(2 * np.pi * rate_hz * t))) ** sharpness


def _master(y, freqs, target_rms=0.22):
    y = _circ_eq(y, freqs, 45.0, 4200.0)
    y = np.tanh(y * 1.35) / np.tanh(1.35)
    y = _circ_eq(y, freqs, 45.0, 4000.0)
    y = y * (target_rms / (np.sqrt(np.mean(y ** 2)) + 1e-9))
    peak = float(np.max(np.abs(y)))
    if peak > 0.88:
        y *= 0.88 / peak
    return y.astype(np.float32)


def make_drill_diamond_whir():
    """Mining drill loop (2.0 s, 44.1 kHz mono): high-torque copper-rotor motor (~124 Hz) + 3rd-order
    rotor harmonic (~372 Hz) + 16 Hz 4-flute modulated diamond-cutting rasp, warm low-pass roll-off."""
    n = int(SR * 2.0)
    t = np.arange(n) / SR
    freqs = np.fft.rfftfreq(n, 1.0 / SR)
    rng = np.random.default_rng(20261123)

    motor = _harm_motor(t, 124.0, [1.0, 0.85, 0.50, 0.28, 0.16, 0.09], lfo_f=4.0, lfo_depth=1.4, rng=rng)
    rotor = _harm_motor(t, 372.0, [0.32, 0.18, 0.09], lfo_f=4.0, lfo_depth=3.5, rng=rng)
    flute_mod = 0.65 + 0.35 * _pulse_train(t, 16.0, 2.5)
    cut = _circ_band_noise(rng, n, freqs, 650, 2300, 2.2) * flute_mod
    low = _circ_band_noise(rng, n, freqs, 150, 550, 2.0) * (0.7 + 0.3 * np.sin(2 * np.pi * 8.0 * t))
    y = 0.50 * motor * (0.82 + 0.18 * np.sin(2 * np.pi * 4.0 * t)) + 0.24 * rotor + 0.36 * cut + 0.25 * low
    return _master(y, freqs, target_rms=0.22)


def write_ogg(rel_path, samples):
    path = os.path.join(OUT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, samples, SR, format='OGG', subtype='VORBIS')
    print(f'wrote {os.path.relpath(path, ROOT)} ({os.path.getsize(path)} bytes, {len(samples) / SR:.2f}s mono)')


def main():
    write_ogg('tool/drill.ogg', make_drill_diamond_whir())


if __name__ == '__main__':
    main()

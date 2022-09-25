#!C:/KaizokuEncoder/python

import vapoursynth as vs
import lvsfunc as lvf
import awsmfunc as awf
from debandshit import dumb3kdb
from vsutil import depth, iterate
from adptvgrnMod import adptvgrnMod
from cooldegrain import CoolDegrain
from vardautomation import (
    FileInfo, X265Encoder, FFmpegAudioExtracter, EztrimCutter, make_comps,
    QAACEncoder, Mux, RunnerConfig, SelfRunner, PresetAAC, PresetBD
)

core = vs.core

exclude_range = [(11507, 13667), (144744, 150300)]
descale_args = dict(height=720, kernel=lvf.kernels.Catrom())

ITBD = FileInfo('00006.m2ts', preset=[PresetBD, PresetAAC])


def filtering():
    clip = depth(ITBD.clip_cut, 16)
    edge = awf.bbmod(clip, 1, 1, 1, 1)

    rescale = lvf.scale.descale(edge, **descale_args)
    rescale = depth(rescale, 16)
    aa = lvf.aa.taa(rescale, lvf.aa.nnedi3())

    denoise = CoolDegrain(aa, thsad=64, blksize=8, overlap=4)
    deband = dumb3kdb(denoise, radius=16, threshold=30)

    detail_mask = lvf.mask.detail_mask(aa, rad=1)
    detail_merge = core.std.MaskedMerge(deband, aa, detail_mask)
    grain = adptvgrnMod(detail_merge, strength=0.1, sharp=64, static=True)

    credit_mask = lvf.scale.descale(edge, show_mask=True, **descale_args)
    credit_mask = depth(iterate(credit_mask, core.std.Inflate, 4), 16)
    restore = core.std.MaskedMerge(depth(grain, 16), depth(edge, 16), credit_mask)
    exclude = lvf.rfs(restore, edge, ranges=exclude_range)

    final = depth(exclude, 10)
    return final


if __name__ == '__main__':
    config = RunnerConfig(
        X265Encoder('settings'),
        a_extracters = FFmpegAudioExtracter(ITBD, track_in=2, track_out=1),
        a_cutters = EztrimCutter(ITBD, track=1),
        a_encoders = QAACEncoder(ITBD, track=1),
        muxer = Mux(ITBD)
    )
    SelfRunner(filtering(), ITBD, config).run()
    make_comps(
        clips = dict(
            src = ITBD.clip_cut,
            flt = filtering(),
            enc = vs.core.ffms2.Source(ITBD.name_file_final.to_str())
        ),
        num = 10,
        path = f'_comps/movie',
        collection_name = f'[Kaizoku] My Hero Academia - World Heroes\' Mission',
        force_bt709 = True,
        slowpics = True,
        public = False
    )
else:
    filtering().set_output()


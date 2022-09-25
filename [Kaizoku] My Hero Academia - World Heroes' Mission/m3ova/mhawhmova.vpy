import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import awsmfunc as awf
from cooldegrain import CoolDegrain
from adptvgrnMod import adptvgrnMod
from debandshit import dumb3kdb
from vsutil import depth

core = vs.core
core.max_cache_size = 50000

src = lvf.src('OVA_BDREMUX.mkv')
src = fvf.Depth(src, 16)
src = awf.bbmod(src, 1, 1, 1, 1)

descale = lvf.scale.descale(src, height=720, kernel=lvf.kernels.Catrom())
descale = depth(descale, 16)

aa_lo = lvf.aa.taa(descale, lvf.aa.nnedi3())
aa_hi = lvf.aa.upscaled_sraa(descale, 1.5)
aa = lvf.aa.clamp_aa(descale, aa_lo, aa_hi)

halo_mask = lvf.mask.halo_mask(aa, brz=0.25)
dehalo = haf.DeHalo_alpha(aa, darkstr=0.5)
merge = core.std.MaskedMerge(aa, dehalo, halo_mask)

denoise = CoolDegrain(merge, thsad=96, blksize=8, overlap=4)
detail_mask = lvf.mask.detail_mask(denoise, brz_a=0.3)
deband = dumb3kdb(denoise, radius=16, threshold=44)
deband = core.std.MaskedMerge(deband, merge, detail_mask)

grain = adptvgrnMod(deband, strength=0.15, cstrength=0.02, size=1.1, sharp=70, luma_scaling=10, static=True)
exclude = lvf.rfs(grain, src, ranges=[(0, 215), (7824, 8200)])

final = depth(exclude, 10)
final.set_output()


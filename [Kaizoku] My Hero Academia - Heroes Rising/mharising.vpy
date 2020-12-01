import vapoursynth as vs
import lvsfunc as lvf
import mvsfunc as mvf
import fvsfunc as fvf
import havsfunc as haf
import kagefunc as kgf
import vsTAAmbk as taa
import nnedi3_rpow2 as nep
from vsutil import get_w

core = vs.get_core()
core.max_cache_size = 15000

vid = lvf.src(r"C:\Users\dedsec\Downloads\Torrents\MHARISING\BDMV\STREAM\00006.m2ts")
src = fvf.Depth(vid, 16)

Y, U, V = kgf.split(src)

scaled = kgf.inverse_scale(Y, height=720, kernel='bicubic', b=0, c=1, mask_detail=True)
scaled = fvf.Depth(nep.nnedi3_rpow2(scaled).resize.Spline36(1920, 1080), 16)
scaled = kgf.join([scaled, U, V])

deband = core.f3kdb.Deband(scaled, range=16, preset="low", grainc=0, output_depth=16)

grain = kgf.adaptive_grain(deband, 0.25)
final = fvf.Depth(grain, 10)
final.set_output()

# i'm well aware that this is a shit script.
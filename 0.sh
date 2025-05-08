python kd.py cops \
       --E0 testdata/raw/Diatom-5-Ed0.csv \
       --Ez testdata/raw/Diatom-5-EdZ.csv \
       --meta testdata/raw/Diatom-5-Metadata.csv \
       --vlEr testdata/intermediate/vlEr-noisy.csv \
       --zmin 0 \
       --zmax 50 \

python kd.py solve-pKd \
    --vlEr testdata/intermediate/vlEr-noisy.csv \
    --pKd  testdata/intermediate/pKd.npz \
    --plEr testdata/intermediate/plEr.npz \
    --dw 12 \
    --dz 100 \

python kd.py make-w \
     --w testdata/intermediate/w.csv \
     --wmin 313 \
     --wmax 765 \
     --num 200 \
    
python kd.py make-tz \
        --tz testdata/intermediate/tz.csv \
	--zmin 0 \
	--zmax 50 \
	--num 200 \

python kd.py eval-poly \
       --poly testdata/intermediate/pKd.npz \
       --w testdata/intermediate/w.csv \
       --tz testdata/intermediate/tz.csv \
       --vals testdata/intermediate/vKd.csv \

python kd.py eval-poly \
       --poly testdata/intermediate/plEr.npz \
       --w testdata/intermediate/w.csv \
       --tz testdata/intermediate/tz.csv \
       --vals testdata/intermediate/vlEr.csv \

python kd.py heatmap \
       --vals testdata/intermediate/vlEr-noisy.csv \
       --out testdata/figures/vlEr-noisy.pdf \

python kd.py heatmap \
       --vals testdata/intermediate/vlEr.csv \
       --out testdata/figures/vlEr.pdf \

python kd.py heatmap \
       --vals testdata/intermediate/vKd.csv \
       --out testdata/figures/vKd.pdf \
       --wrap log \

python kd.py slices \
    --plEr testdata/intermediate/plEr.npz \
    --vlEr testdata/intermediate/vlEr-noisy.csv \
    --out testdata/figures/vlEr-slices.pdf \

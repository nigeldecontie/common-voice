#!/bin/sh
readonly indir=${1:?You must provide a source directory}
readonly outdir=${2:?You must provide a target directory}

# convert to pcm
for f in $indir/*.wav; do
   sox \
      --type sw \
      --channel 1 \
      --rate 48k \
      $f \
      "${f%.wav}.pcm"
done

mv $indir/*.pcm $outdir/

# denoise
for f in $outdir/*.pcm; do
   rnnoise $f ${f%.pcm}.raw;
done

# convert back to wav
for f in $outdir/*.raw; do
   sox \
      --type raw \
      --channels 1 \
      --rate 48k \
      --bits 16 \
      --encoding signed \
      $f \
      "${f%.raw}.wav"
done

rm $outdir/*.raw
rm $outdir/*.pcm

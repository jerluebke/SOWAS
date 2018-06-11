#!/bin/zsh

file='eq'
prefix='\\def\\formula{'
postfix="}\\input{${file}.tex}"

eqs=('\\dot{\\phi}_{as}'
     'v_{as}(\\lambda, \\dot{\\phi}_{as}) = \\frac{\\lambda + h}{t} \\text{, } t = \\int_0^{\\psi}
     \\frac{\\mathrm{d}\\theta}{\\dot{\\theta}(\\theta, \\lambda, \\dot{\\phi}_{as})}'
     '\\dot{\\phi}_{i+1} = \\dot{\\phi}_i \\sqrt{\\left(\\frac{k-1}{k}\\right)
     \\left(1-\\frac{1}{k}\\frac{P}{K_i}\\right)}'
     'k = \\sum_{i=1}^N \\frac{K_i}{K_1} = \\sum_{i=1}^N \\left(\\frac{\\dot{\\theta}_{i+1}}
     {\\dot{\\theta}_1}\\right)^2 = 1 + \\sum_{j=1}^N \\prod_{i=1}^j \\left(
     \\frac{\\dot{\\theta}_{i+1}}{\\dot{\\theta}_i} \\right)^2')

names=('phi_dot_as' 'v_as' 'phi_dot_seq' 'k')

for ((idx=1;idx<=${#eqs[@]};idx++))
do
    cmd="${prefix}${eqs[${idx}]}${postfix}"
    name=${names[${idx}]}
    echo $cmd > "${name}.tex"
    pdflatex "${name}.tex"
    convert -density 300 "${name}.pdf" -quality 90 "${name}.png"

    # cleanup
    for type in "aux" "log" "pdf" "tex"
    do
        rm "${name}.${type}"
    done
done


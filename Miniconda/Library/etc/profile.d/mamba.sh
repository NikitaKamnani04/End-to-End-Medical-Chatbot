export MAMBA_ROOT_PREFIX="C:/End-to-End-Medical-Chatbot/Miniconda/Library"
__mamba_setup="$("C:/End-to-End-Medical-Chatbot/Miniconda/Library/bin/mamba" shell hook --shell posix 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__mamba_setup"
else
    alias mamba="C:/End-to-End-Medical-Chatbot/Miniconda/Library/bin/mamba"  # Fallback on help from mamba activate
fi
unset __mamba_setup

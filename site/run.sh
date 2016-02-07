if [ -d dist ]
then
    timestamp=`date +%Y%m%d%H%M%S`
    directory=backup/$timestamp
    mkdir -p "$directory"
    mv dist/* "$directory"
fi

gulp
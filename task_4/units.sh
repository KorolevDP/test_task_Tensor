#!/bin/bash

# Получаем список юнитов с именем foobar-
units=$(systemctl list-units --type=service --all | grep 'foobar-' | awk '{print $1}')

# Проходим по каждому юниту
for unit in $units; do
    # Останавливаем юнит
    echo "Stopping $unit..."
    systemctl stop "$unit"

    # Извлекаем название сервиса из имени юнита
    service_name=${unit#foobar-}

    # Определяем рабочую директорию и новую директорию
    working_dir="/opt/misc/$service_name"
    new_dir="/srv/data/$service_name"

    # Переносим файлы
    echo "Moving files from $working_dir to $new_dir..."
    mv "$working_dir" "$new_dir"

    # Обновляем конфигурацию юнита
    unit_file="/etc/systemd/system/$unit"
    
    if [ -f "$unit_file" ]; then
        # Создаем временный файл для изменения конфигурации
        temp_file=$(mktemp)

        # Изменяем пути в параметрах WorkingDirectory и ExecStart
        while IFS= read -r line; do
            if [[ $line == WorkingDirectory=* ]]; then
                echo "WorkingDirectory=$new_dir" >> "$temp_file"
            elif [[ $line == ExecStart=* ]]; then
                echo "ExecStart=$new_dir/$(basename ${line#ExecStart=})" >> "$temp_file"
            else
                echo "$line" >> "$temp_file"
            fi
        done < "$unit_file"

        # Заменяем старый файл новым
        mv "$temp_file" "$unit_file"

        # Перезагружаем конфигурацию systemd
        systemctl daemon-reload

        # Запускаем юнит снова
        echo "Starting $unit..."
        systemctl start "$unit"
    else
        echo "Unit file for $unit not found!"
    fi

done

echo "All services have been processed."
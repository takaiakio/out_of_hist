import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CSVUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            
            # ヘッダラベルの取得
            headers = df.columns
            
            # 統計データの計算
            stats = {}
            for header in headers:
                if pd.api.types.is_numeric_dtype(df[header]):
                    mean = round(df[header].mean(), 2)
                    std = round(df[header].std(), 2)
                    stats[header] = {'mean': mean, 'std': std}
                    
                    # ヒストグラムの作成
                    plt.figure(figsize=(10, 6))
                    plt.hist(df[header].dropna(), bins=30, edgecolor='k')
                    plt.title(f'Histogram of {header}')
                    plt.xlabel(header)
                    plt.ylabel('Frequency')
                    
                    # ヒストグラムを画像として保存
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    plt.close()
                    stats[header]['histogram'] = img_str

            return render(request, 'csv_analysis/results.html', {'stats': stats})
    else:
        form = CSVUploadForm()
    return render(request, 'csv_analysis/upload.html', {'form': form})

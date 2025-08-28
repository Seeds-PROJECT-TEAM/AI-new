import pandas as pd
from pathlib import Path

def read_excel_schema():
    """테이블 정의서 Excel 파일 읽기"""
    excel_file = Path(__file__).resolve().parents[2] / "_테이블 정의서.xlsx"
    
    if not excel_file.exists():
        print(f"❌ 파일을 찾을 수 없음: {excel_file}")
        return
    
    try:
        # Excel 파일의 모든 시트 읽기
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        print(f"📋 Excel 파일 읽기 완료: {len(excel_data)}개 시트")
        
        for sheet_name, df in excel_data.items():
            print(f"\n📊 시트: {sheet_name}")
            print(f"   행 수: {len(df)}")
            print(f"   컬럼: {list(df.columns)}")
            
            if len(df) > 0:
                # 테이블명 컬럼의 고유값 확인
                if len(df.columns) > 0:
                    first_col = df.iloc[:, 0]
                    unique_tables = first_col.dropna().unique()
                    print(f"\n   발견된 테이블들:")
                    
                    # 학습 경로 관련 테이블 찾기
                    learning_tables = []
                    for table in unique_tables:
                        table_str = str(table).lower()
                        if any(keyword in table_str for keyword in ['learning', 'path', 'diagnostic', 'test', 'result', 'answer', 'concept', 'unit']):
                            learning_tables.append(table)
                        elif '테이블명' not in str(table) and pd.notna(table):
                            print(f"     - {table}")
                    
                    if learning_tables:
                        print(f"\n   🎯 학습 경로 관련 테이블들:")
                        for table in learning_tables:
                            print(f"     - {table}")
                    
                    # 각 테이블의 상세 구조 분석
                    print(f"\n   📋 테이블별 상세 구조:")
                    current_table = None
                    table_structure = {}
                    
                    for i in range(len(df)):
                        row = df.iloc[i]
                        if pd.notna(row.iloc[0]):
                            cell_value = str(row.iloc[0])
                            
                            # 새로운 테이블 시작
                            if '테이블명' not in cell_value and pd.notna(row.iloc[0]) and '(' in cell_value:
                                current_table = cell_value
                                table_structure[current_table] = []
                                print(f"\n     📊 {current_table}:")
                            
                            # 테이블 속성 정보
                            elif current_table and pd.notna(row.iloc[1]) and pd.notna(row.iloc[2]):
                                attr_name = row.iloc[1]
                                data_type = row.iloc[2]
                                required = row.iloc[3] if pd.notna(row.iloc[3]) else "선택"
                                description = row.iloc[4] if pd.notna(row.iloc[4]) else ""
                                
                                if pd.notna(attr_name) and pd.notna(data_type):
                                    print(f"       {attr_name}: {data_type} ({required}) - {description}")
                                    table_structure[current_table].append({
                                        'attribute': attr_name,
                                        'type': data_type,
                                        'required': required,
                                        'description': description
                                    })
            
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    read_excel_schema()

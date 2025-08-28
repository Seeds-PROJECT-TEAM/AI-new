#!/usr/bin/env python3
"""
diagnostic_analysis 테이블 구조 확인
"""

import pandas as pd

def check_diagnostic_schema():
    """diagnostic_analysis 테이블 구조 확인"""
    try:
        # Excel 파일 읽기
        df = pd.read_excel('_테이블 정의서.xlsx')
        
        # diagnostic_analysis 테이블 찾기
        diagnostic_rows = df[df.iloc[:, 0].str.contains('diagnostic_analysis', na=False)]
        
        if len(diagnostic_rows) > 0:
            start_idx = diagnostic_rows.index[0]
            print(f"🔍 diagnostic_analysis 테이블 시작 위치: {start_idx}")
            
            # diagnostic_analysis 테이블의 모든 필드 확인
            print(f"📋 diagnostic_analysis 테이블 구조:")
            print("=" * 80)
            
            # 헤더 출력
            print(f"{'행':<3} | {'필드명':<25} | {'설명':<25} | {'데이터타입':<20} | {'필수여부':<15} | {'설명'}")
            print("-" * 80)
            
            for i in range(start_idx, start_idx + 20):  # 최대 20행 확인
                if i >= len(df):
                    break
                    
                row = df.iloc[i]
                
                # 모든 컬럼의 값 확인
                col0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
                col1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                col2 = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
                col3 = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                col4 = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
                
                # 다음 테이블 시작인지 확인
                if i > start_idx and ('unit' in col0 or 'problem' in col0):
                    print(f"   -> 다음 테이블 시작: {col0}")
                    break
                
                # 빈 행이 아닌 경우 출력
                if any([col0, col1, col2, col3, col4]):
                    print(f"{i:3d} | {col0:<25} | {col1:<25} | {col2:<20} | {col3:<15} | {col4}")
        else:
            print("❌ diagnostic_analysis 테이블을 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_diagnostic_schema()

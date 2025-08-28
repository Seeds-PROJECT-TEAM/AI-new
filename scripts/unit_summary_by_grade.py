#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nerdmath 데이터베이스의 unit 컬렉션에서 학년별 Unit 개수를 요약하여 표로 보여주는 스크립트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from collections import defaultdict
from tabulate import tabulate

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

class UnitSummaryAnalyzer:
    def __init__(self):
        self.client = None
        self.db = None
        self.mongodb_uri = os.getenv("MONGODB_URI")
        
        if not self.mongodb_uri:
            raise RuntimeError("MONGODB_URI 환경변수가 설정되지 않았습니다.")
    
    def connect(self):
        """MongoDB에 연결"""
        try:
            print("🚀 MongoDB 연결 시도 중...")
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client.nerdmath
            self.client.admin.command("ping")
            print("✅ MongoDB 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ MongoDB 연결 실패: {e}")
            return False
    
    def get_unit_summary_by_grade(self):
        """학년별 Unit 개수 요약"""
        try:
            unit_collection = self.db.unit
            
            # 전체 Unit 개수 확인
            total_units = unit_collection.count_documents({})
            print(f"📊 전체 Unit 개수: {total_units}개")
            
            # 학년별 Unit 개수 집계
            pipeline = [
                {
                    "$group": {
                        "_id": "$grade",
                        "count": {"$sum": 1},
                        "units": {"$push": {
                            "unitId": "$unitId",
                            "title": "$title",
                            "chapter": "$chapter",
                            "chapterTitle": "$chapterTitle"
                        }}
                    }
                },
                {
                    "$sort": {"_id": 1}  # 학년 순으로 정렬
                }
            ]
            
            grade_summary = list(unit_collection.aggregate(pipeline))
            
            if not grade_summary:
                print("❌ Unit 데이터가 없습니다.")
                return None
            
            return grade_summary
            
        except Exception as e:
            print(f"❌ Unit 요약 조회 실패: {e}")
            return None
    
    def display_summary_table(self, grade_summary):
        """학년별 요약을 표로 출력"""
        try:
            # 표 데이터 준비
            table_data = []
            
            for grade_info in grade_summary:
                grade = grade_info["_id"]
                count = grade_info["count"]
                units = grade_info["units"]
                
                # 단원 정보 정리
                unit_details = []
                for unit in units:
                    title_ko = unit["title"].get("ko", "제목 없음") if isinstance(unit["title"], dict) else str(unit["title"])
                    unit_details.append(f"{unit['chapter']}. {title_ko}")
                
                table_data.append({
                    "학년": grade,
                    "Unit 개수": count,
                    "단원 목록": "\n".join(unit_details)
                })
            
            # pandas DataFrame으로 변환
            df = pd.DataFrame(table_data)
            
            # 표 출력
            print("\n" + "="*80)
            print("📚 학년별 Unit 개수 요약")
            print("="*80)
            
            # 학년별 개수 요약
            summary_df = df[["학년", "Unit 개수"]].copy()
            print("\n📊 학년별 Unit 개수:")
            print(tabulate(summary_df, headers="keys", tablefmt="grid", showindex=False))
            
            # 전체 통계
            total_units = df["Unit 개수"].sum()
            print(f"\n🎯 전체 Unit 개수: {total_units}개")
            print(f"📈 평균 Unit 개수: {total_units / len(df):.1f}개/학년")
            
            # 상세 단원 목록
            print("\n📋 학년별 상세 단원 목록:")
            print("="*80)
            
            for _, row in df.iterrows():
                print(f"\n🎓 {row['학년']}학년 ({row['Unit 개수']}개 단원)")
                print("-" * 40)
                print(row['단원 목록'])
            
            return df
            
        except Exception as e:
            print(f"❌ 표 출력 실패: {e}")
            return None
    
    def get_chapter_summary(self, grade_summary):
        """챕터별 요약 정보"""
        try:
            chapter_stats = defaultdict(int)
            
            for grade_info in grade_summary:
                units = grade_info["units"]
                for unit in units:
                    chapter = unit["chapter"]
                    chapter_stats[chapter] += 1
            
            print("\n📖 챕터별 Unit 분포:")
            print("-" * 30)
            
            # 챕터별 데이터를 표로 출력
            chapter_data = []
            for chapter in sorted(chapter_stats.keys()):
                count = chapter_stats[chapter]
                percentage = (count / sum(chapter_stats.values())) * 100
                chapter_data.append([f"챕터 {chapter}", count, f"{percentage:.1f}%"])
            
            print(tabulate(chapter_data, headers=["챕터", "Unit 개수", "비율"], tablefmt="grid"))
            
        except Exception as e:
            print(f"❌ 챕터 요약 실패: {e}")
    
    def analyze_units(self):
        """Unit 분석 실행"""
        try:
            # 1. 학년별 요약 조회
            grade_summary = self.get_unit_summary_by_grade()
            if not grade_summary:
                return False
            
            # 2. 표로 출력
            df = self.display_summary_table(grade_summary)
            if df is None:
                return False
            
            # 3. 챕터별 요약
            self.get_chapter_summary(grade_summary)
            
            return True
            
        except Exception as e:
            print(f"❌ Unit 분석 실패: {e}")
            return False
    
    def close(self):
        """MongoDB 연결 종료"""
        if self.client:
            self.client.close()
            print("\n🔌 MongoDB 연결 종료")

def main():
    """메인 함수"""
    print("🚀 Unit 학년별 요약 분석 시작")
    print("=" * 60)
    
    analyzer = None
    try:
        analyzer = UnitSummaryAnalyzer()
        
        if not analyzer.connect():
            print("❌ MongoDB 연결 실패")
            return
        
        success = analyzer.analyze_units()
        
        if success:
            print("\n🎉 Unit 학년별 요약 분석 완료!")
        else:
            print("\n❌ Unit 분석 실패!")
            
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if analyzer:
            analyzer.close()

if __name__ == "__main__":
    main()

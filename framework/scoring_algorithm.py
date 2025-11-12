"""
Operational Equity Framework - Scoring Algorithm

This module calculates scores from framework assessments and generates
interpretive reports.

Author: Marshawn Shelton, MPH, PMP, CCMP
Organization: Isosalus
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime

class EquityFrameworkScorer:
    """
    Score Operational Equity Framework assessments and generate reports.
    """
    
    def __init__(self, questions_file: str = 'framework/assessment_questions.json'):
        """
        Initialize scorer with assessment questions.
        
        Parameters
        ----------
        questions_file : str
            Path to JSON file containing assessment questions
        """
        with open(questions_file, 'r') as f:
            self.assessment_data = json.load(f)
        
        self.metadata = self.assessment_data['metadata']
        self.scoring_guide = self.assessment_data['scoring_guide']
        self.pillars = ['PROCESS', 'PEOPLE', 'TECHNOLOGY']
        
        print(f"✅ Loaded {self.metadata['total_questions']} questions")
        print(f"   Framework: {self.metadata['framework_name']} v{self.metadata['version']}")
    
    def get_questions_for_pillar(self, pillar: str) -> List[Dict]:
        """
        Get all questions for a specific pillar.
        
        Parameters
        ----------
        pillar : str
            Pillar name (PROCESS, PEOPLE, or TECHNOLOGY)
            
        Returns
        -------
        list of dict
            Questions for the specified pillar
        """
        return self.assessment_data[pillar]['questions']
    
    def calculate_question_score(self, question: Dict, response: str) -> int:
        """
        Calculate score for a single question based on response.
        
        Parameters
        ----------
        question : dict
            Question data including scoring rules
        response : str
            User's response to the question
            
        Returns
        -------
        int
            Score for this question (0-5)
        """
        scoring = question['scoring']
        return scoring.get(response, 0)
    
    def calculate_pillar_score(self, pillar: str, responses: Dict[str, str]) -> Tuple[int, int, float]:
        """
        Calculate score for an entire pillar.
        
        Parameters
        ----------
        pillar : str
            Pillar name
        responses : dict
            Mapping of question IDs to responses
            
        Returns
        -------
        tuple
            (points_earned, max_points, percentage_score)
        """
        questions = self.get_questions_for_pillar(pillar)
        total_points = 0
        max_points = len(questions) * 5  # 5 points per question
        
        for question in questions:
            question_id = question['id']
            if question_id in responses:
                response = responses[question_id]
                points = self.calculate_question_score(question, response)
                total_points += points
        
        percentage = (total_points / max_points) * 100 if max_points > 0 else 0
        
        return total_points, max_points, percentage
    
    def calculate_overall_score(self, responses: Dict[str, str]) -> Dict:
        """
        Calculate scores for all pillars and overall assessment.
        
        Parameters
        ----------
        responses : dict
            Complete set of responses {question_id: response}
            
        Returns
        -------
        dict
            Complete scoring breakdown with interpretation
        """
        results = {
            'assessment_date': datetime.now().strftime('%Y-%m-%d'),
            'pillars': {},
            'overall': {}
        }
        
        pillar_scores = []
        
        # Calculate each pillar
        for pillar in self.pillars:
            points, max_points, percentage = self.calculate_pillar_score(pillar, responses)
            
            results['pillars'][pillar] = {
                'points_earned': points,
                'max_points': max_points,
                'percentage': round(percentage, 1),
                'interpretation': self._interpret_score(percentage)
            }
            
            pillar_scores.append(percentage)
            
            print(f"\n{pillar}:")
            print(f"   Score: {points}/{max_points} ({percentage:.1f}%)")
            print(f"   {self._interpret_score(percentage)}")
        
        # Calculate overall
        overall_percentage = sum(pillar_scores) / len(pillar_scores)
        
        results['overall'] = {
            'percentage': round(overall_percentage, 1),
            'interpretation': self._interpret_score(overall_percentage),
            'pillar_breakdown': {p: results['pillars'][p]['percentage'] for p in self.pillars}
        }
        
        print(f"\n{'='*60}")
        print(f"OVERALL SCORE: {overall_percentage:.1f}%")
        print(f"INTERPRETATION: {self._interpret_score(overall_percentage)}")
        print(f"{'='*60}")
        
        return results
    
    def _interpret_score(self, percentage: float) -> str:
        """
        Interpret a percentage score using scoring guide rubric.
        
        Parameters
        ----------
        percentage : float
            Score percentage (0-100)
            
        Returns
        -------
        str
            Interpretation text
        """
        if percentage <= 40:
            return self.scoring_guide['interpretation']['0-40']
        elif percentage <= 60:
            return self.scoring_guide['interpretation']['41-60']
        elif percentage <= 80:
            return self.scoring_guide['interpretation']['61-80']
        else:
            return self.scoring_guide['interpretation']['81-100']
    
    def identify_gaps(self, responses: Dict[str, str], threshold: int = 2) -> Dict[str, List[Dict]]:
        """
        Identify questions scoring below threshold (gaps to address).
        
        Parameters
        ----------
        responses : dict
            Assessment responses
        threshold : int, default 2
            Score threshold (questions scoring <= threshold are flagged)
            
        Returns
        -------
        dict
            Gaps by pillar with question details
        """
        gaps = {pillar: [] for pillar in self.pillars}
        
        for pillar in self.pillars:
            questions = self.get_questions_for_pillar(pillar)
            
            for question in questions:
                question_id = question['id']
                if question_id in responses:
                    response = responses[question_id]
                    score = self.calculate_question_score(question, response)
                    
                    if score <= threshold:
                        gaps[pillar].append({
                            'id': question_id,
                            'question': question['question'],
                            'response': response,
                            'score': score,
                            'max_score': 5,
                            'rationale': question['rationale']
                        })
        
        return gaps
    
    def generate_summary_report(self, responses: Dict[str, str], organization_name: str = "Organization") -> None:
        """
        Generate a text-based summary report.
        
        Parameters
        ----------
        responses : dict
            Assessment responses
        organization_name : str
            Name of organization being assessed
        """
        print("\n" + "="*80)
        print(f"OPERATIONAL EQUITY FRAMEWORK ASSESSMENT REPORT")
        print(f"Organization: {organization_name}")
        print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
        print("="*80)
        
        # Calculate scores
        results = self.calculate_overall_score(responses)
        
        # Identify gaps
        print(f"\n{'='*80}")
        print("PRIORITY GAPS (Questions scoring ≤2 points)")
        print("="*80)
        
        gaps = self.identify_gaps(responses, threshold=2)
        
        for pillar in self.pillars:
            pillar_gaps = gaps[pillar]
            if pillar_gaps:
                print(f"\n{pillar} ({len(pillar_gaps)} gaps):")
                for gap in pillar_gaps[:5]:  # Show top 5
                    print(f"\n  • {gap['question']}")
                    print(f"    Current: {gap['response']} ({gap['score']}/5 points)")
                    print(f"    Why it matters: {gap['rationale']}")
        
        # Recommendations
        print(f"\n{'='*80}")
        print("RECOMMENDATIONS")
        print("="*80)
        
        self._generate_recommendations(results)
    
    def _generate_recommendations(self, results: Dict) -> None:
        """
        Generate prioritized recommendations based on scores.
        
        Parameters
        ----------
        results : dict
            Scoring results from calculate_overall_score
        """
        # Find lowest scoring pillar
        pillar_scores = [(p, results['pillars'][p]['percentage']) for p in self.pillars]
        pillar_scores.sort(key=lambda x: x[1])
        
        lowest_pillar = pillar_scores[0][0]
        lowest_score = pillar_scores[0][1]
        
        print(f"\nPRIORITY FOCUS AREA: {lowest_pillar}")
        print(f"Current Score: {lowest_score:.1f}%")
        print(f"\nThis pillar represents your greatest opportunity for improvement.")
        
        # Pillar-specific recommendations
        recommendations = {
            'PROCESS': [
                "Review and document all care pathways with equity lens",
                "Implement language accessibility across scheduling and service delivery",
                "Add evening/weekend appointment availability",
                "Establish transportation assistance programs",
                "Integrate community health workers into care teams"
            ],
            'PEOPLE': [
                "Implement mandatory equity training for 100% of staff annually",
                "Tie equity metrics to performance evaluations",
                "Hire and retain workforce representative of patient population",
                "Establish Chief Equity Officer position with budget authority",
                "Create equity champion network across departments"
            ],
            'TECHNOLOGY': [
                "Enable real-time outcome stratification by race/ethnicity in EHR",
                "Implement automated risk alerts for maternal health conditions",
                "Deploy multilingual patient portal",
                "Establish monthly equity dashboard reporting to leadership",
                "Conduct equity impact assessments for all new technology"
            ]
        }
        
        print(f"\nRecommended Actions for {lowest_pillar}:")
        for i, rec in enumerate(recommendations[lowest_pillar], 1):
            print(f"  {i}. {rec}")
        
        # Overall recommendation
        overall_score = results['overall']['percentage']
        
        print(f"\n{'='*80}")
        print("OVERALL ASSESSMENT")
        print("="*80)
        
        if overall_score < 40:
            print("\n⚠️  CRITICAL: Significant operational gaps exist across all three pillars.")
            print("   Recommendation: Engage comprehensive assessment and 6-month")
            print("   implementation support to build foundational infrastructure.")
        elif overall_score < 60:
            print("\n⚡ MODERATE: Infrastructure exists but significant improvement needed.")
            print("   Recommendation: Focus on lowest-scoring pillar first, then address")
            print("   cross-pillar integration.")
        elif overall_score < 80:
            print("\n✓ STRONG: Solid infrastructure with targeted improvement opportunities.")
            print("   Recommendation: Address specific gaps identified, benchmark against")
            print("   best-in-class organizations.")
        else:
            print("\n🌟 BEST-IN-CLASS: Comprehensive operational equity infrastructure.")
            print("   Recommendation: Share practices with peer organizations, pursue")
            print("   publication of success factors.")


def load_sample_responses() -> Dict[str, str]:
    """
    Create sample responses for testing the scoring system.
    
    Returns
    -------
    dict
        Sample responses for a moderate-scoring organization
    """
    # This represents a typical health system with some equity efforts
    # but significant gaps (expected score: 50-60%)
    
    responses = {
        # PROCESS - Mixed responses (some good, many gaps)
        'P1': 'Yes',
        'P2': 'Annually',
        'P3': '26-50%',
        'P4': 'Assessed but not addressed',
        'P5': 'No',
        'P6': '51-75%',
        'P7': 'Manual coordination',
        'P8': 'Yes',
        'P9': '0-25%',
        'P10': 'Recommended but not required',
        'P11': 'Yes',
        'P12': 'Identified but no enhanced pathway',
        'P13': 'No',
        'P14': '2 modalities',
        'P15': 'No',
        'P16': 'No',
        'P17': '26-50%',
        'P18': 'Reactive (when problems arise)',
        'P19': 'Yes',
        'P20': 'Surveys only',
        
        # PEOPLE - Moderate efforts, accountability gaps
        'PE1': '51-75%',
        'PE2': 'No',
        'PE3': 'No',
        'PE4': '26-50%',
        'PE5': 'Some from community',
        'PE6': '26-50%',
        'PE7': 'No',
        'PE8': 'No',
        'PE9': 'Yes',
        'PE10': '26-50%',
        'PE11': 'No',
        'PE12': 'Available upon request',
        'PE13': 'Somewhat representative',
        'PE14': 'No',
        'PE15': '51-75%',
        'PE16': 'Quarterly',
        'PE17': 'Yes',
        'PE18': 'No',
        'PE19': '26-50%',
        'PE20': 'No',
        
        # TECHNOLOGY - Basic systems, limited stratification
        'T1': 'No',
        'T2': '51-75%',
        'T3': 'No',
        'T4': 'Partial integration',
        'T5': '1-2 languages',
        'T6': '26-50%',
        'T7': 'No',
        'T8': 'No',
        'T9': 'Under development',
        'T10': 'Collected inconsistently',
        'T11': 'No',
        'T12': 'No',
        'T13': 'No',
        'T14': '0-25%',
        'T15': 'No',
        'T16': 'Ad hoc sharing',
        'T17': 'Yes',
        'T18': 'No',
        'T19': 'Annual reports only',
        'T20': 'No'
    }
    
    return responses


if __name__ == "__main__":
    """
    Test the scoring algorithm with sample data.
    """
    print("="*80)
    print("OPERATIONAL EQUITY FRAMEWORK - SCORING ALGORITHM TEST")
    print("="*80)
    
    # Initialize scorer
    scorer = EquityFrameworkScorer()
    
    # Load sample responses
    print("\n📋 Loading sample assessment responses...")
    responses = load_sample_responses()
    print(f"✅ Loaded {len(responses)} responses")
    
    # Generate report
    print("\n📊 Generating assessment report...")
    scorer.generate_summary_report(responses, organization_name="Sample Health System")
    
    print("\n✅ Scoring algorithm test complete!")
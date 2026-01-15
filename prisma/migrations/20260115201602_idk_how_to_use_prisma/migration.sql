/*
  Warnings:

  - Added the required column `blueWinCount` to the `Event` table without a default value. This is not possible if the table is not empty.
  - Added the required column `redWinCount` to the `Event` table without a default value. This is not possible if the table is not empty.
  - Made the column `pointsScored` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `averagePointsPerMatch` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `rpEarned` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `penaltyPoints` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `autoPoints` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `matchesPlayed` on table `Event` required. This step will fail if there are existing NULL values in that column.
  - Made the column `feetClimbed` on table `Event` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "Event" ADD COLUMN     "blueWinCount" INTEGER NOT NULL,
ADD COLUMN     "redWinCount" INTEGER NOT NULL,
ALTER COLUMN "pointsScored" SET NOT NULL,
ALTER COLUMN "averagePointsPerMatch" SET NOT NULL,
ALTER COLUMN "rpEarned" SET NOT NULL,
ALTER COLUMN "penaltyPoints" SET NOT NULL,
ALTER COLUMN "autoPoints" SET NOT NULL,
ALTER COLUMN "matchesPlayed" SET NOT NULL,
ALTER COLUMN "feetClimbed" SET NOT NULL;
